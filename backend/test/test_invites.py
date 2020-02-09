from time import sleep

from portalbackend import app
from portalbackend.models import Invites
from portalbackend.orgs.models import Org
from .conftest import myheaders


def test_post_invites(client, token_v2, app_context):
    test_email = 'iurii.aleev@incountry.com'
    rv = client.post(
        f"/v2/orgs/testtesttest/invites", json={'email': test_email},
        headers=myheaders(token_v2)
    )
    assert rv.status_code == 404  # Organization does not exist
    rv = client.post(
        "/v2/orgs", json={"name": "Test org", "country": "US"},
        headers=myheaders(token_v2))
    assert rv.status_code == 200
    data = rv.get_json()
    org_uuid = data['id']
    rv = client.post(
        f"/v2/orgs/{org_uuid}/invites", json={},
        headers=myheaders(token_v2)
    )
    assert rv.status_code == 400  # Missing email

    rv = client.post(
        f"/v2/orgs/{org_uuid}/invites", json={'email': test_email},
        headers=myheaders(token_v2)
    )
    assert rv.status_code == 200
    invite = Invites.query.filter_by(invited_email=test_email).first()
    assert invite
    rv = client.post(
        f"/v2/orgs/{org_uuid}/invites", json={'email': test_email},
        headers=myheaders(token_v2)
    )
    assert rv.status_code == 400
    rv = client.post(
        f"/v2/orgs/{org_uuid}/invites",
        json={'email': test_email, 'resend': True},
        headers=myheaders(token_v2)
    )
    assert rv.status_code == 200
    result_invites = Invites.query.filter_by(invited_email=test_email).all()
    assert len(result_invites) == 2
    assert Invites.CANCELED in [_.status for _ in result_invites]
    assert Invites.OPEN in [_.status for _ in result_invites]

    rv = client.get(
        f"/v2/invites/fake_token", json={},
        headers=myheaders(token_v2)
    )
    assert rv.status_code == 404

    rv = client.get(
        f"/v2/invites/{invite.invite_token}", json={},
        headers=myheaders(token_v2)
    )
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['email'] == test_email


def test_invite_user(client, token_v2, mocker):
    email = 'new.employee@incountry.com'
    mocker.patch(
        "portalbackend.routes_v2.recaptcha_is_valid", return_value=True
    )
    with app.app_context():
        org_uuid = Org.query.first().uuid
        rv = client.post(
            f"/v2/orgs/{org_uuid}/invites", json={'email': email},
            headers=myheaders(token_v2)
        )
        data = rv.get_json()
        invite_token = (
            Invites.query.filter_by(id=data['id']).first().invite_token
        )
        pw = 'Qwerty12#$'
        rv = client.post(
            "/v2/users",
            json={
                "email": email,
                "username": email,
                "password": pw,
                "country": "IN",
                "inviteToken": invite_token,
                "tos": True,
                "marketing": False,
                "recaptcha": "12445",
            },
        )
        assert rv.status_code == 200


def test_get_invites(client, token_v2):
    rv = client.get(
        f"/v2/orgs/testtesttest/invites", json={},
        headers=myheaders(token_v2)
    )
    assert rv.status_code == 404  # Organization does not exist

    rv = client.post(
        "/v2/orgs", json={"name": "Test org", "country": "US"},
        headers=myheaders(token_v2))
    assert rv.status_code == 200
    data = rv.get_json()
    org_uuid = data['id']

    test_email = 'iurii.aleev@incountry.com'
    real_invite_expiration = app.config.get('USER_INVITATION_EXPIRATION')
    app.config['USER_INVITATION_EXPIRATION'] = 1
    rv = client.post(
        f"/v2/orgs/{org_uuid}/invites", json={'email': test_email},
        headers=myheaders(token_v2)
    )
    assert rv.status_code == 200

    sleep(1)

    rv = client.get(
        f"/v2/orgs/{org_uuid}/invites", json={},
        headers=myheaders(token_v2)
    )
    data = rv.get_json()

    app.config['USER_INVITATION_EXPIRATION'] = real_invite_expiration
    assert rv.status_code == 200
    new_invite = [x for x in data['invites'] if x['email'] == test_email]
    assert len(new_invite) > 0
    assert new_invite[0]['status'] == Invites.EXPIRED


def test_remove_invite_user_from_org(client, token_v2):
    email = 'new.employee123@incountry.com'
    with app.app_context():
        org_uuid = Org.query.first().uuid
        rv = client.post(
            f"/v2/orgs/{org_uuid}/invites", json={'email': email},
            headers=myheaders(token_v2)
        )
        assert rv.status_code == 200
        rv = client.get(
            f"/v2/orgs/{org_uuid}/invites", json={},
            headers=myheaders(token_v2)
        )
        data = rv.get_json()
        new_invite = [x for x in data['invites'] if x['email'] == email]
        assert len(new_invite) > 0
        assert new_invite[0]['status'] == Invites.OPEN
        rv = client.delete(
            f"/v2/orgs/{org_uuid}/invites", json={'email': email},
            headers=myheaders(token_v2)
        )
        assert rv.status_code == 200

        rv = client.get(
            f"/v2/orgs/{org_uuid}/invites", json={},
            headers=myheaders(token_v2)
        )
        assert rv.status_code == 200
        data = rv.get_json()
        invite = [x for x in data['invites'] if x['email'] == email]
        assert len(invite) > 0
        assert invite[0]['status'] == Invites.CANCELED


def test_post_get_delete_joinlink_in_org(client, token_v2):
    email = 'new.employee123@incountry.com'
    with app.app_context():
        org_uuid = Org.query.first().uuid

        # lets create Invite with email
        rv = client.post(
            f"/v2/orgs/{org_uuid}/invites", json={'email': email},
            headers=myheaders(token_v2)
        )
        assert rv.status_code == 200

        rv = client.post(
            f"/v2/orgs/{org_uuid}/joinlinks", json={},
            headers=myheaders(token_v2)
        )
        assert rv.status_code == 200
        data = rv.get_json()
        token = data['invite_token']

        rv = client.get(
            f"/v2/orgs/{org_uuid}/joinlinks", json={},
            headers=myheaders(token_v2)
        )
        assert rv.status_code == 200
        data = rv.get_json()
        assert 'joinlink' in data
        joinlink = data['joinlink']
        assert joinlink['invite_token'] == token
        assert joinlink['status'] == Invites.OPEN

        rv = client.delete(
            f"/v2/orgs/{org_uuid}/joinlinks", json={},
            headers=myheaders(token_v2)
        )
        assert rv.status_code == 200

        rv = client.get(
            f"/v2/orgs/{org_uuid}/joinlinks", json={},
            headers=myheaders(token_v2)
        )
        assert rv.status_code == 200
        data = rv.get_json()
        assert 'joinlink' in data
        joinlink = data['joinlink']
        assert joinlink['invite_token'] == token
        assert joinlink['status'] == Invites.CANCELED

        rv = client.get(
            f"/v2/orgs/{org_uuid}/invites", json={},
            headers=myheaders(token_v2)
        )
        assert rv.status_code == 200
        data = rv.get_json()
        invite = [x for x in data['invites'] if x['email'] == email]
        assert len(invite) > 0
        assert invite[0]['status'] == Invites.OPEN

from portalbackend import app, bcrypt
from portalbackend.models import User

from .conftest import confirm_user_email, myheaders


def test_create_user_and_check_key(client, mocker):
    mocker.patch(
        "portalbackend.routes_v2.recaptcha_is_valid", return_value=True
    )
    email = "scooter3@example.com"
    pw = "secret3!"
    client.post(
        "/v2/users",
        json={
            "email": email,
            "username": email,
            "password": pw,
            "country": "IN",
            "company": "Apple",
            "tos": True,
            "recaptcha": "12445",
        },
    )

    # Force confirm the email
    with app.app_context():
        confirm_user_email(client, User.query.filter_by(email=email).first())

    rv = client.post("/login", json={"email": email, "password":pw})
    assert rv.status_code == 200

    auth_token = rv.get_json()['auth_token']

    # Now load the User and verify that is has an Org, Zone and ZoneAPIKey
    with app.app_context():
        user = User.query.filter_by(email = email).first()
        assert user is not None

        assert len(user.orgs) > 0

        org = user.orgs[0]

        assert len(org.zones) > 0

        zone = org.zones[0]

        assert len(zone.api_keys) > 0

        apikey = zone.api_keys[0]

        assert app._consul._confirm_key_registered_v3(zone.uuid, apikey.prefix)

        assert app._consul.verify_key_in_zone_v3("us", zone.uuid, apikey.composite_id, bcrypt)


def test_create_user_and_check_key_v3(client, mocker):
    mocker.patch(
        "portalbackend.routes_v2.recaptcha_is_valid", return_value=True
    )
    email = "scooter3@example.com"
    pw = "secret3!"
    client.post(
        "/v2/users",
        json={
            "email": email,
            "username": email,
            "password": pw,
            "country": "IN",
            "company": "Apple",
            "tos": True,
            "recaptcha": "12445",
        },
    )

    # Force confirm the email
    with app.app_context():
        confirm_user_email(client, User.query.filter_by(email=email).first())

    rv = client.post("/login", json={"email": email, "password":pw})
    assert rv.status_code == 200

    auth_token = rv.get_json()['auth_token']

    # Now load the User and verify that is has an Org, Zone and ZoneAPIKey
    with app.app_context():
        user = User.query.filter_by(email = email).first()
        assert user is not None

        assert len(user.orgs) > 0

        org = user.orgs[0]

        assert len(org.zones) > 0

        zone = org.zones[0]

        assert len(zone.api_keys) > 0

        apikey = zone.api_keys[0]

        # FIXME: Turn these on when V3 keys are finished
        assert app._consul._confirm_key_registered_v3(zone.uuid, apikey.prefix)
        assert app._consul.verify_key_in_zone_v3("us", zone.uuid, apikey.composite_id, bcrypt)


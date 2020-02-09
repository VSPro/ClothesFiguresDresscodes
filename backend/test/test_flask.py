import time
from urllib.parse import urlparse

from portalbackend import app, db
from portalbackend.models import User
from portalbackend.orgs.models import Org
from .conftest import confirm_user_email, myheaders


# Fixtures


# Tests


def test_countries(client):
    rv = client.get("/countries")
    assert rv.status_code == 200


def test_countries_secret(client):
    rv = client.get("/countries_secret")
    assert rv.status_code == 401


def test_resource_not_found(client):
    rv = client.get("/nopage")
    assert rv.status_code == 404


def test_register_must_have_email(client):
    rv = client.post("/v2/users", json={"password": "secret"})
    assert rv.status_code == 400


def test_register_must_have_password(client):
    rv = client.post("/v2/users", json={"email": "scottp@example.com"})
    assert rv.status_code == 400


def test_register(client, mocker):
    mocker.patch(
        "portalbackend.routes_v2.recaptcha_is_valid", return_value=True
    )
    email = "scottp@example.com"
    rv = client.post(
        "/v2/users",
        json={
            "email": email,
            "username": email,
            "password": "secret3!",
            "country": "IN",
            "company": "IBM",
            "tos": True,
            "recaptcha": "12445",
        },
    )
    assert rv.status_code == 200
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        assert user is not None


def test_user_bcrypt(client, app_context):
    user = User(username='user1', email='test@test.com', password='test**8++')
    assert user.check_password("test**8++")
    db.session.add(user)
    db.session.commit()
    assert user.check_password("test**8++")

    u2 = User.query.filter_by(email=user.email).first()
    assert u2.check_password("test**8++")


def test_login(client, mocker):
    mocker.patch(
        "portalbackend.routes_v2.recaptcha_is_valid", return_value=True
    )
    email = "scooter@examle.com"
    pw = "secret2@"

    rv = client.post(
        "/v2/users",
        json={
            "email": email,
            "username": email,
            "password": pw,
            "country": "IN",
            "company": "IBM",
            "tos": True,
            "recaptcha": "12445",
        },
    )
    assert rv.status_code == 200

    with app.app_context():
        u2 = User.query.filter_by(email=email).first()
        assert u2.check_password(pw)

        # test email reconfirmation
        app.user_manager.USER_CONFIRM_EMAIL_EXPIRATION = 0.1
        token = app.user_manager.generate_token(u2.id)
        time.sleep(1)
        rv = client.get("/confirm-email/" + token)
        assert rv.status_code == 401
        rv = client.post("/overridden_resend_user_confirm")
        assert rv.status_code == 400
        rv = client.post("/overridden_resend_user_confirm", json={'email': email})
        assert rv.status_code == 200
        app.user_manager.USER_CONFIRM_EMAIL_EXPIRATION = app.config['USER_CONFIRM_EMAIL_EXPIRATION']

        rv = confirm_user_email(client, u2)
        assert rv.status_code == 200 or rv.status_code == 302

        u2 = User.query.filter_by(email=email).first()
        assert u2.email_confirmed_at is not None

    # Validation process works here, return 400
    assert client.post("/login", json={}).status_code == 400
    assert client.post("/login", json={"email": email}).status_code == 400
    assert client.post("/login", json={"email": email, "pw": pw}).status_code == 400

    # Wrong email, password combination
    assert client.post("/login", json={"email": email, "password": "wrong"}).status_code == 401

    rv = client.post("/login", json={"email": email, "password": pw})
    assert rv.status_code == 200

    data = rv.get_json()
    assert 'auth_token' in data
    assert 'user_id' in data
    assert 'user_name' in data


def test_get_api_key(client, token):
    rv = client.get("/api_key", headers=myheaders(token))
    assert 'api_key' in rv.get_json()


def test_edit_user_profile(client, token):
    # No token
    rv = client.patch("/v2/user/profile")
    assert rv.status_code == 401

    # Bad token
    rv = client.patch(
        "/v2/user/profile",
        headers={"Authorization": ("Bearer " + "a bad token")},
    )
    assert rv.status_code == 401

    # Good token, but no data
    rv = client.patch("/v2/user/profile", headers=myheaders(token))
    assert rv.status_code == 404

    rv = client.patch(
        "/v2/user/profile",
        headers=myheaders(token),
        json={"password": "VeryValidPassw0rd!"},
    )
    assert rv.status_code == 404

    rv = client.patch(
        "/v2/user/profile",
        headers=myheaders(token),
        json={"email": "alex@incountry.com"},
    )
    assert rv.status_code == 404

    rv = client.patch(
        "/v2/user/profile",
        headers=myheaders(token),
        json={"company": "InCountry"},
    )
    assert rv.status_code == 200

    rv = client.patch(
        "/v2/user/profile", headers=myheaders(token), json={"country": "AU"}
    )
    assert rv.status_code == 200

    with app.app_context():
        user_id = User.decode_auth_token(token)['sub']
        u = User.query.filter_by(id=user_id).first()
        assert u.company == 'InCountry'

    rv = client.patch(
        "/v2/user/profile",
        headers=myheaders(token),
        json={"company": "Microsoft"},
    )
    assert rv.status_code == 200

    with app.app_context():
        user_id = User.decode_auth_token(token)['sub']
        u = User.query.filter_by(id=user_id).first()
        assert u.company == 'Microsoft'

        org = Org(name='Amazon')
        db.session.add(org)
        db.session.commit()
        rv = client.patch(
            "/v2/user/profile",
            headers=myheaders(token),
            json={"default_org": org.uuid},
        )
        assert rv.status_code == 404

        rv = client.patch(
            "/v2/user/profile",
            headers=myheaders(token),
            json={"default_org": "459395"},
        )
        assert rv.status_code == 404

        rv = client.post(
            "/v2/orgs",
            json={"name": "My New Co.", "country": "UA"},
            headers=myheaders(token),
        )
        new_default_org_id = rv.get_json()['id']
        rv = client.patch(
            "/v2/user/profile",
            headers=myheaders(token),
            json={"default_org": new_default_org_id},
        )
        assert rv.status_code == 200
        new_org = Org.query.filter_by(uuid=new_default_org_id).first()
        rev_u = User.query.filter_by(id=user_id).first()
        assert rev_u.default_org_id == new_org.id


def test_redirector(client):
    rv = client.post("/redirect/v2/storage/records/us")
    assert rv.status_code == 307
    parts = urlparse(rv.location)

    assert parts.hostname == 'us.api.incountry.io'
    assert parts.path == '/v2/storage/records/us'


def test_change_email(client, token):
    rv = client.post(
        "/change_email",
        headers=myheaders(token),
        json={"email": "user@incountry.com"},
    )
    assert rv.status_code == 200

    rv = client.post("/change_email", headers=myheaders(token))
    assert rv.status_code == 400

    rv = client.post(
        "/confirm_old_email",
        headers=myheaders(token),
        json={"email": "user@incountry.com"},
    )
    assert rv.status_code == 400

    rv = client.post(
        "/confirm_old_email",
        headers=myheaders(token),
        json={"email": "user@incountry.com", 'token': '123'},
    )
    assert rv.status_code == 404

    with app.app_context():
        resp = User.decode_auth_token(token)
    email_token = app.user_manager.generate_token(resp['sub'])
    rv = client.post(
        "/confirm_old_email",
        headers=myheaders(token),
        json={"email": "user@incountry.com", 'token': email_token},
    )
    assert rv.status_code == 200

    rv = client.post("/confirm_old_email", headers=myheaders(token))
    assert rv.status_code == 400

    rv = client.post(
        "/confirm_new_email",
        headers=myheaders(token),
        json={"email": "user@incountry.com", 'token': '123'},
    )
    assert rv.status_code == 404

    rv = client.post("/confirm_new_email", headers=myheaders(token))
    assert rv.status_code == 400

    with app.app_context():
        resp = User.decode_auth_token(token)
    email_token = app.user_manager.generate_token(resp['sub'])

    rv = client.post(
        "/confirm_new_email",
        headers=myheaders(token),
        json={"email": "user@incountry.com", 'token': email_token},
    )
    assert rv.status_code == 200

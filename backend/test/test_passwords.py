
import time
from datetime import datetime, timedelta

from portalbackend import app
from portalbackend.models import User, db

from .conftest import confirm_user_email, myheaders

# Fixtures


def test_change_password(client, token):
    rv = client.post("/password")
    assert rv.status_code == 401

    rv = client.post("/password", headers=myheaders(token), json={})
    assert rv.status_code == 400

    rv = client.post(
        "/password",
        headers=myheaders(token),
        json={"oldPassword": "bad value", "newPassword": "newvalue"},
    )
    assert rv.status_code == 400

    # Password change has a 2 second backdating to make testing easier.
    # In this case we just created our JWT, so let's wait through the
    # backdate window so we can verify that changing the password expires
    # the token.
    time.sleep(2)

    change_time = datetime.utcnow() - timedelta(seconds=2)

    # No symbol pass
    new_pw = "Dream weaver 6"
    rv = client.post(
        "/password",
        headers=myheaders(token),
        json={"oldPassword": "secret3!", "newPassword": new_pw},
    )
    assert rv.status_code == 422

    # No number pass
    new_pw = "Dream weaver %"
    rv = client.post(
        "/password",
        headers=myheaders(token),
        json={"oldPassword": "secret3!", "newPassword": new_pw},
    )
    assert rv.status_code == 422

    # Less than 8 chars pass
    new_pw = "Dream6%"
    rv = client.post(
        "/password",
        headers=myheaders(token),
        json={"oldPassword": "secret3!", "newPassword": new_pw},
    )
    assert rv.status_code == 422

    # Test error message
    new_pw = "Dream6%"
    rv = client.post(
        "/password",
        headers=myheaders(token),
        json={"oldPassword": "secret3!", "newPassword": new_pw},
    )
    assert b'Password Validation Error' in rv.data

    # Good pass
    new_pw = "Dream weaver 6 %"
    rv = client.post(
        "/password",
        headers=myheaders(token),
        json={"oldPassword": "secret3!", "newPassword": new_pw},
    )
    assert rv.status_code == 200

    with app.app_context():
        user_id = User.decode_auth_token(token)['sub']
        u = User.query.filter_by(id=user_id).first()
        assert u.password_changed_at > change_time

        # JWT tokens should be invalidated
        rv = client.get("/countries_secret", headers=myheaders(token))
        assert rv.status_code == 401

        # So login again
        rv = client.post("/login", json={"email": u.email, "password": new_pw})
        assert rv.status_code == 200

        # and make sure the new token works
        data = rv.get_json()
        token = data['auth_token']
        rv = client.get("/countries_secret", headers=myheaders(token))
        assert rv.status_code == 200


def test_password_reset(client, mocker):
    mocker.patch(
        "portalbackend.routes_v2.recaptcha_is_valid", return_value=True
    )
    rv = client.post("/password/request_reset")
    assert rv.status_code == 400  # missing email

    email = "scottp@incountry.com"
    old_pw = "secret3!"
    rv = client.post(
        "/v2/users",
        json={
            "email": email,
            "username": email,
            "password": old_pw,
            "country": "IN",
            "company": "IBM",
            "tos": True,
            "recaptcha": "12445",
        },
    )
    assert rv.status_code == 200

    # Force confirm the email
    with app.app_context():
        confirm_user_email(client, User.query.filter_by(email=email).first())

    # swizzle the generate_token function so we can capture the token
    orig_generate_token = getattr(
        app.user_manager.token_manager.__class__, 'generate_token'
    )

    def capture_generate_token(self, value):
        saved_token = orig_generate_token(
            app.user_manager.token_manager, value
        )
        setattr(client, '__token', saved_token)
        return saved_token

    setattr(
        app.user_manager.token_manager.__class__,
        'generate_token',
        capture_generate_token,
    )

    # We should intercept the email so we can simulate clicking the link
    rv = client.post("/password/request_reset", json={"email": email})
    assert rv.status_code == 200

    # make sure the token capture worked
    assert client.__token is not None

    # Reset password, user never logged in
    rv = client.post(
        "/password/confirm_reset",
        json={"token": client.__token},
    )
    assert rv.status_code == 200

    # Login to get a token
    rv = client.post("/login", json={"email": email, "password": old_pw})

    # failure cases
    assert client.post("/password/reset", json={}).status_code == 400
    assert (
        client.post("/password/reset", json={"token": "123"}).status_code
        == 400
    )
    assert (
        client.post(
            "/password/reset",
            json={"token": "123", "newPassword": "newish"},
        ).status_code
        == 400
    )

    # bad values to confirm
    assert (
        client.post(
            "/password/confirm_reset",
            json={"token": "bad"},
        ).status_code
        == 401
    )
    assert (
        client.post(
            "/password/confirm_reset",
            json={"token": client.__token},
        ).status_code
        == 401
    )

    # Validate that token
    rv = client.post(
        "/password/confirm_reset",
        json={"token": client.__token},
    )
    assert rv.status_code == 200

    # Finally! We can collect new password from the user, then actually
    # reset the password
    new_pw = "!newer_55_password!"
    rv = client.post(
        "/password/reset",
        json={
            "token": client.__token,
            "newPassword": new_pw,
        },
    )
    assert rv.status_code == 200

    # Login with the old password doesn't work
    assert (
        client.post(
            "/login", json={"email": email, "password": old_pw}
        ).status_code
        == 401
    )

    # BUt login with the new one works
    rv = client.post("/login", json={"email": email, "password": new_pw})
    assert rv.status_code == 200
    assert 'auth_token' in rv.get_json()


def test_password_generator(client, mocker):
    mocker.patch(
        "portalbackend.routes_v2.recaptcha_is_valid", return_value=True
    )
    email = "scottp@incountry.com"
    old_pw = "secret3!"
    rv = client.post(
        "/v2/users",
        json={
            "email": email,
            "username": email,
            "password": old_pw,
            "country": "IN",
            "company": "IBM",
            "tos": True,
            "recaptcha": "12445",
        },
    )
    assert rv.status_code == 200

    # Force confirm the email
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        confirm_user_email(client, user)

    rv = client.post("/password/request_reset", json={
        "email": email,
        "autogenerate": True,
        "one_time_password": True
    })
    assert rv.status_code == 200

    with app.app_context():
        user = User.query.filter_by(email=email).first()

    assert user.one_time_password

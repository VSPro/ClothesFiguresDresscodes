import datetime
import json

import pytest
from flask import url_for

from portalbackend import app
from portalbackend.models import User
from .conftest import confirm_user_email, myheaders


def test_health(client):
    rv = client.get("/health")
    assert rv.status_code == 200

    data = rv.get_json()
    assert 'status' in data
    assert data['status'] == 'OK'


def test_url_for_override():
    """
    When we send emails we need to spoof URL construction so that it points to
    the React app instead of the backend server. This test just verifies that
    our hack to do that works properly.
    """
    with app.test_request_context(base_url=app.config['FRONTEND_SERVER']):
        url = url_for('user.confirm_email', token="faketoken", _external=True)
        assert url.startswith(app.config['FRONTEND_SERVER'])


def test_registration_with_good_data(client, generate_registration_data, mocker):
    mocker.patch(
        "portalbackend.routes_v2.recaptcha_is_valid", return_value=True
    )

    rv = client.post("/v2/users", json=generate_registration_data())
    assert rv.status_code == 200


@pytest.mark.parametrize("key, err_code, err_source", [
    ('email', 'ERR_VALIDATION', "{'email': ['Missing data for required field.']}"),

    ('username', 'ERR_VALIDATION', "{'username': ['Missing data for required field.']}"),

    ('password', 'ERR_VALIDATION', "{'password': ['Missing data for required field.']}"),

    ('tos', 'ERR_VALIDATION', "{'tos': ['Missing data for required field.']}"),

    ('recaptcha', 'ERR_VALIDATION', "{'recaptcha': ['Missing data for required field.']}"),

    ('marketing', 'ERR_VALIDATION', "{'marketing': ['Missing data for required field.']}"),

    ('country', 'ERR_VALIDATION', "{'country': ['Missing data for required field.']}"),
])
def test_registration_required_parameter_is_absent(client, generate_registration_data, key, err_code, err_source):
    data = generate_registration_data()
    del data[key]

    rv = client.post("/v2/users", json=data)
    assert rv.status_code == 400

    error = json.loads(rv.data.decode())["errors"][0]
    assert error["code"] == err_code
    assert error["source"] == err_source


@pytest.mark.parametrize("key, value, err_code, err_source", [
    ('wrong_param', 'some_value', 'ERR_VALIDATION', "{'wrong_param': ['Unknown field.']}"),
])
def test_registration_wrong_parameter_exist(client, generate_registration_data, key,
                                            value, err_code, err_source):
    data = generate_registration_data()
    data[key] = value

    rv = client.post("/v2/users", json=data)
    assert rv.status_code == 400

    error = json.loads(rv.data.decode())["errors"][0]
    assert error["code"] == 'ERR_VALIDATION'
    assert error["source"] == "{'wrong_param': ['Unknown field.']}"


@pytest.mark.parametrize("key, value, err_code, err_source", [
    ('email', 'localhost', 'ERR_VALIDATION', "{'email': ['Not a valid email address.']}"),

    ('username', 'locahost', 'ERR_VALIDATION', "{'username': ['Not a valid email address.']}"),

    # TODO check password complexity
    ('password', 'qwe123', 'ERR_VALIDATION', "{'password': ['Length must be between 8 and 128.']}"),

    ('tos', '11', 'ERR_VALIDATION', "{'tos': ['Not a valid boolean.']}"),
    ('tos', False, 'ERR_TENANT', "User should accept TOS"),

    ('recaptcha', 78576857, 'ERR_VALIDATION', "{'recaptcha': ['Not a valid string.']}"),

    ('marketing', 11111, 'ERR_VALIDATION', "{'marketing': ['Not a valid boolean.']}"),

    ('country', 'ttt', 'ERR_VALIDATION', "{'country': ['Length must be 2.']}"),
    ('country', 'TT', 'ERR_TENANT', "Wrong country code: TT"),
])
def test_registration_wrong_parameter_value(client, generate_registration_data, mocker,
                                            key, value, err_code, err_source):
    mocker.patch("portalbackend.routes_v2.recaptcha_is_valid", return_value=True)

    data = generate_registration_data()
    data[key] = value

    rv = client.post("/v2/users", json=data)
    assert rv.status_code == 400

    error = json.loads(rv.data.decode())["errors"][0]
    assert error["code"] == err_code
    assert error["source"] == err_source


def test_registration_company_and_invite_both_present(client, generate_registration_data, mocker):
    mocker.patch("portalbackend.routes_v2.recaptcha_is_valid", return_value=True)

    data = generate_registration_data(company='Alabama', inviteToken='Token form Alabama')
    rv = client.post("/v2/users", json=data)
    assert rv.status_code == 400

    error = json.loads(rv.data.decode())["errors"][0]
    assert error["code"] == 'ERR_TENANT'
    assert error["source"] == "Got both. Send only company or inviteTicket"


def test_registration_company_and_invite_both_absent(client, generate_registration_data, mocker):
    mocker.patch("portalbackend.routes_v2.recaptcha_is_valid", return_value=True)

    data = generate_registration_data()
    del data['company']
    rv = client.post("/v2/users", json=data)
    assert rv.status_code == 400

    error = json.loads(rv.data.decode())["errors"][0]
    assert error["code"] == 'ERR_TENANT'
    assert error["source"] == "Got both. Send only company or inviteTicket"


def test_register(client, mocker):
    mocker.patch(
        "portalbackend.routes_v2.recaptcha_is_valid", return_value=True
    )
    email = "scottp@example.com"
    pw = "secret3!"

    rv = client.post("/v2/users",
                     json={"email": email, "username": email, "password": pw, "country": "IN"})
    assert rv.status_code == 400  # must have company

    rv = client.post(
        "/v2/users",
        json={
            "email": email,
            "username": email,
            "password": pw,
            "country": "IN",
            "company": "IBM",
        },
    )
    assert rv.status_code == 400  # must agree with tos

    rv = client.post(
        "/v2/users",
        json={
            "email": email,
            "username": email,
            "password": pw,
            "country": "IN",
            "company": "IBM",
            "tos": False,
        },
    )
    assert rv.status_code == 400  # must agree with tos

    rv = client.post(
        "/v2/users",
        json={
            "email": email,
            "username": email,
            "password": pw,
            "country": "IN",
            "company": "IBM",
            "tos": True,
            "marketing": False,  # ok to not opt in to marketing
            "recaptcha": "12445",
        },
    )
    assert rv.status_code == 200
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        assert len(user.memberships) > 0
        confirm_user_email(client, user)
        assert type(user.tos_timestamp) is datetime.datetime
        assert user.marketing_timestamp is None

    email2 = "another@example.com"
    rv = client.post(
        "/v2/users",
        json={
            "email": email2,
            "username": email2,
            "password": pw,
            "country": "IN",
            "company": "IBM",
            "tos": True,
            "marketing": True,  # ok to not opt in to marketing
            "recaptcha": "12445",
        },
    )
    assert rv.status_code == 200
    with app.app_context():
        user = User.query.filter_by(email=email2).first()
        assert user.marketing_timestamp is not None

    rv = client.post("/login", json={"email": email, "password": pw})
    assert rv.status_code == 200

    data = rv.get_json()
    assert 'auth_token' in data


def test_me(client, token_v2):
    rv = client.get("/v2/me", headers=myheaders(token_v2))
    assert rv.status_code == 200
    data = rv.get_json()

    assert 'email' in data
    assert 'uuid' in data
    assert 'default_org' in data
    assert data['default_org'] is not None
    assert 'country' in data['orgs'][0]
    assert 'role' in data['orgs'][0]
    assert 'default_org_role' in data
    assert 'default_org_name' in data


def test_git_commit(client):
    rv = client.get("/v2/git_commit")
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'git_commit' in data
    assert data['git_commit'] == app.config['GIT_COMMIT']

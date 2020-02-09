import functools
import json
import os

import pytest
from flask import g

from .helpers import RegistrationDataGenerator

# NOTE: LEAVE THIS LINE HERE!! THIS NEEDS TO HAPPEN **BEFRORE** WE IMPORT 'app'
# since that import will import config.py and setup the database connection
os.environ['DB_DATABASE'] = 'portalbackend_test'  # noqa: E402

from portalbackend import app, db
from portalbackend.models import User, UsageSummary

# This fixture requires an HTTP test client, but ALSO manages clearing data
# in the db between tests. You should probably include this fixture in
# every test.


@pytest.fixture
def client():
    client = app.test_client()

    app.config['DEBUG'] = True
    app.config['TESTING'] = True

    with app.app_context():
        if not hasattr(g, 'db'):
            g.db = db
            db.session.close()
            db.drop_all()
            db.create_all()
        else:
            db.session.query(User).delete()
            db.session.query(UsageSummary).delete()
            db.session.commit()

    yield client


@pytest.fixture
def app_context():
    with app.app_context():
        yield


@pytest.fixture
def token(client, mocker):
    """Creates a new user, confirms its email, and logs in to get an
    auth token."""
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
            "company": "IBM",
            "tos": True,
            "marketing": False,
            "recaptcha": "12445",
        },
    )

    # Force confirm the email
    with app.app_context():
        confirm_user_email(client, User.query.filter_by(email=email).first())

    rv = client.post("/login", json={"email": email, "password": pw})
    assert rv.status_code == 200

    auth_token = rv.get_json()['auth_token']
    yield auth_token


@pytest.fixture
def token_v2(client, mocker):
    """Creates a new user, confirms its email, and logs in to get an auth token."""
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
            "marketing": False,
            "recaptcha": "12445",
        },
    )
    # Force confirm the email
    with app.app_context():
        confirm_user_email(client, User.query.filter_by(email=email).first())

    rv = client.post("/login", json={"email": email, "password": pw})
    assert rv.status_code == 200

    auth_token = rv.get_json()['auth_token']
    yield auth_token


def confirm_user_email(client, user):
    if user is None:
        raise ValueError("Attempting to confirm user email, but model is None")
    token = app.user_manager.generate_token(user.id)
    return client.get("/confirm-email/" + token)


def myheaders(token):
    return {"Authorization": ("Bearer " + token), "Content-Type": "application/json"}


@pytest.fixture(scope='session')
def countries():
    try:
        data = json.loads(app._consul._consul.kv.get("service/poplist")[1]['Value'].decode())
        return [item['id'] for item in data['countries']]
    except:
        return ['US']


@pytest.fixture
def generate_registration_data(countries):
    generator = RegistrationDataGenerator()
    return functools.partial(generator, countries=countries)

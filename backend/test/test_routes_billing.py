import pytest
import stripe

from portalbackend import app
from portalbackend.models import User, PROFESSIONAL_PLAN, TRIAL_PLAN
from portalbackend.orgs.models import OrgMember
from .conftest import confirm_user_email, myheaders


@pytest.fixture
def token_billing(client, mocker):
    """Creates a new user, confirms its email, and logs in to get an auth token."""
    mocker.patch(
        "portalbackend.routes_v2.recaptcha_is_valid", return_value=True
    )
    email = "scooter3@example.com"
    pw = "secret3!"
    org = "scooter"
    country = "CY"
    client.post(
        "/v2/users",
        json={
            "email": email,
            "username": email,
            "password": pw,
            "country": "IN",
            "company": "IBM",
            "tos": True,
            "recaptcha": "12445",
            "marketing": True
        },
    )
    client.post("/v2/orgs", json={"name": org, "country": country})

    # Force confirm the email
    with app.app_context():
        confirm_user_email(client, User.query.filter_by(email=email).first())

    rv = client.post("/login", json={"email": email, "password": pw})
    assert rv.status_code == 200

    auth_token = rv.get_json()['auth_token']
    yield auth_token

# Tests


def test_get_account(client, token_billing):
    rv = client.get("/billing/account", json={}, headers=myheaders(token_billing))
    assert rv.status_code == 200
    assert rv.get_json()['plan'] == TRIAL_PLAN


def test_post_subscription(client, token_billing, app_context):
    test_plan = 'plan_FQeOkevvZWUZfs'
    user = User.query.filter_by(email='scooter3@example.com').first()
    orgmember = OrgMember.query.filter_by(user_id=user.id).first()
    rv = client.post(f"/v2/orgs/{orgmember.org.uuid}/subscriptions", json={
        'plan': PROFESSIONAL_PLAN,
        'stripe_token': 'test_token'
    }, headers=myheaders(token_billing))
    assert rv.status_code == 200
    result = rv.get_json()
    assert result == f'No such token: test_token'

    rv = client.post(f"/v2/orgs/{orgmember.org.uuid}/subscriptions", json={
        'plan': PROFESSIONAL_PLAN,
        'stripe_token': 'tok_1EvQcMCbPY9jRQdj4MsNjxkR'
    }, headers=myheaders(token_billing))
    assert rv.status_code == 200
    result = rv.get_json()
    assert result == 'You cannot use a Stripe token more than once: tok_1EvQcMCbPY9jRQdj4MsNjxkR.'

    stripe.api_key = app.config.get('STRIPE_API_PUBLIC_KEY')
    response = stripe.Token.create(
      card={
        'number': '4242424242424242',
        'exp_month': 12,
        'exp_year': 2020,
        'cvc': '123',
      },
    )

    # lets use configurated plan
    real_basic_plan = app.config.get('STRIPE_BASIC_PLAN')
    app.config['STRIPE_BASIC_PLAN'] = test_plan
    rv = client.post(f"/v2/orgs/{orgmember.org.uuid}/subscriptions", json={
        'email': 'chak-chak@uslugi.tatarstan.ru',
        'username': 'Mintimer',
        'addressLine1': 'Cool Sheriff',
        'addressLine2': 'Kazan Kremlin',
        'city': 'Kazan',
        'country': 'Russian Federation',
        'state': 'Tatarstan Republic',
        'zipCode': '420000',
        'plan': PROFESSIONAL_PLAN,
        'stripe_token': response['id']
    }, headers=myheaders(token_billing))
    app.config['STRIPE_BASIC_PLAN'] = real_basic_plan
    assert rv.status_code == 200
    result = rv.get_json()
    assert 'id' in result


def test_update_customer(client, token_billing):
    rv = client.post("/billing/update_customer", json={}, headers=myheaders(token_billing))
    assert rv.status_code == 400  # Missing customerId


def test_update_customer_card(client, token_billing):
    rv = client.post("/billing/update_customer_card", json={}, headers=myheaders(token_billing))
    assert rv.status_code == 400  # Missing customerId
    rv = client.post("/billing/update_customer_card", json={'customerId': 123}, headers=myheaders(token_billing))
    assert rv.status_code == 400  # Missing source


def test_update_subscription(client, token_billing):
    rv = client.post("/billing/update_subscription", json={}, headers=myheaders(token_billing))
    assert rv.status_code == 400  # Missing itemId
    rv = client.post("/billing/update_subscription", json={'itemId': 123}, headers=myheaders(token_billing))
    assert rv.status_code == 400  # Missing planId


def test_cancel_subscription(client, token_billing):
    rv = client.delete("/billing/cancel_subscription", headers=myheaders(token_billing))
    assert rv.status_code == 400  # Missing subscriptionId


def test_get_pricing_plan(client, token_billing):
    rv = client.get("/billing/get_pricing_plan", headers=myheaders(token_billing))
    assert rv.status_code == 200
    data = rv.get_json()
    assert len(data['plans']) > 0
    assert all(x in data['plans'][0] for x in (
        'name', 'monthly_price', 'records_included',
        'additional_record_price', 'api_calls_included', 'bandwidth_mb'))


def test_get_customer_data(client, token_billing):
    rv = client.get("/billing/customer", headers=myheaders(token_billing))
    assert rv.status_code == 200

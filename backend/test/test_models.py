from portalbackend import db
from portalbackend.models import APIKey, User

# Fixtures


def test_encode_auth_token(client, app_context):
    user = User(
        username='test@test.com', email='test@test.com', password='==test89'
    )
    db.session.add(user)
    db.session.commit()
    auth_token = user.encode_auth_token(user.id)
    assert isinstance(auth_token, bytes)


def test_decode_auth_token(client, app_context):
    user = User(username='user1', email='test@test.com', password='te--4st||')
    db.session.add(user)
    db.session.commit()
    auth_token = user.encode_auth_token(user.id)
    assert isinstance(auth_token, bytes)
    assert User.decode_auth_token(auth_token)['sub'] == user.id


def test_api_key(client, app_context):
    user = User(
        username='test@test.com', email='test@test.com', password='?8tes<>t'
    )
    db.session.add(user)

    api_key = APIKey(
        usage_plan_id='123', api_key_id='123', plan_key_id='123', api_key='123'
    )
    user.api_keys.append(api_key)

    db.session.add(api_key)
    db.session.commit()

    u2 = User.query.filter_by(id=user.id).first()
    assert len(u2.api_keys) > 0
    assert any([x.check_apikey('123') for x in u2.api_keys])
    assert any([x.api_key_raw == '123' for x in u2.api_keys])

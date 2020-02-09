from portalbackend import db, app
from portalbackend.models import User
from portalbackend.orgs.models import Org, OrgMember, OrgSchemaTableColumn, Roles, Notifications
from .conftest import myheaders


def test_create_org(client, token_v2):
    rv = client.post("/v2/orgs", json={"name": "ACME org"}, headers=myheaders(token_v2))
    assert rv.status_code == 400  # missing country

    rv = client.post(
        "/v2/orgs", json={"name": "ACME org", "country": "US"},
        headers=myheaders(token_v2))
    assert rv.status_code == 200

    data = rv.get_json()
    assert 'id' in data
    assert 'name' in data
    assert 'zones' in data
    assert len(data['zones']) > 0

    real_limit = app.config.get('LIMIT_ORG_OWNERSHIP')
    app.config['LIMIT_ORG_OWNERSHIP'] = 1
    rv = client.post(
        "/v2/orgs", json={"name": "Limit org ownerships", "country": "US"},
        headers=myheaders(token_v2))
    assert rv.status_code == 403
    app.config['LIMIT_ORG_OWNERSHIP'] = real_limit


def test_get_org(client, token_v2):
    with app.app_context():
        rv = client.get(f"/v2/orgs/some_org", headers=myheaders(token_v2))
        assert rv.status_code == 404

        org = Org.query.first()
        rv = client.get(f"/v2/orgs/{org.uuid}", headers=myheaders(token_v2))
        assert rv.status_code == 200
        data = rv.get_json()
        assert 'id' in data
        assert data['id'] == org.uuid


def test_update_org(client, token_v2):
    with app.app_context():
        org = Org.query.first()
        rv = client.patch(f"/v2/orgs/{org.uuid}", headers=myheaders(token_v2))
        assert rv.status_code == 400
        assert b'ERR_HTTP_BODY_SIZE' in rv.data
        rv = client.patch(
            f"/v2/orgs/sfsdfkjh4re",
            headers=myheaders(token_v2),
            json={"country": "UA"},
        )
        assert rv.status_code == 404
        rv = client.patch(
            f"/v2/orgs/{org.uuid}",
            headers=myheaders(token_v2),
            json={"country": "UA", "name": "EPAM"},
        )
        assert rv.status_code == 200
        rev_org = Org.query.filter_by(id=org.id).first()
        assert rev_org.name == 'EPAM'
        assert rev_org.home_country == 'UA'


def test_soft_delete_org(client, token_v2, mocker):
    mocker.patch(
        "portalbackend.routes_v2.recaptcha_is_valid", return_value=True
    )
    with app.app_context():
        rv = client.delete(f"/v2/orgs/12345", headers=myheaders(token_v2))
        assert rv.status_code == 404

        client.post(
            "/v2/users",
            json={
                "email": "pedro@apple.com",
                "username": "pedro@apple.com",
                "password": "qwerty89*(",
                "country": "IN",
                "company": "Apple",
                "tos": True,
                "marketing": False,
                "recaptcha": "12445",
            },
        )
        user2 = User.query.filter_by(username='pedro@apple.com').first()
        org = Org.query.first()
        org_uuid = org.uuid
        org.org_members.append(OrgMember(user=user2, role=Roles.MEMBER.value))  # noqa: E501
        db.session.add(user2)
        db.session.commit()
        rv = client.delete(f"/v2/orgs/{org_uuid}", headers=myheaders(token_v2))
        assert rv.status_code == 400  # more than one user in org

        rv = client.delete(
            f"/v2/orgs/{org_uuid}/users/{user2.uuid}", headers=myheaders(token_v2)  # noqa: E501
        )
        assert rv.status_code == 200

        rv = client.delete(f"/v2/orgs/{org_uuid}", headers=myheaders(token_v2))
        assert rv.status_code == 200
        rev_org = (
            Org.query.filter_by(uuid=org_uuid)
            .execution_options(include_deleted=True)
            .first()
        )
        assert rev_org.deleted is True
        assert len(rev_org.org_members) == 0


def test_get_users(client, token_v2):
    rv = client.get(
        f"/v2/orgs/testtesttest/users", json={},
        headers=myheaders(token_v2)
    )
    assert rv.status_code == 404  # Organization does not exist

    rv = client.post(
        "/v2/orgs", json={"name": "Test org", "country": "US"},
        headers=myheaders(token_v2))
    assert rv.status_code == 200
    data = rv.get_json()
    org_uuid = data['id']
    rv = client.get(
        f"/v2/orgs/{org_uuid}/users", json={},
        headers=myheaders(token_v2)
    )
    assert rv.status_code == 200

    user = rv.get_json()['users'][0]
    assert user['invite_type'] is not None
    assert user['invite_type'] == 'Invite Link'


def test_patch_users(client, token_v2):
    with app.app_context():
        org = Org.query.first()

        rv = client.patch(
            f"v2/orgs/{org.uuid}/users/11111",
            headers=myheaders(token_v2),
            json={'role': 'product'}
        )
        assert rv.status_code == 404

        user = User()
        user.username = 'Member 1'
        user.email = 'member@test.com'
        user.password = 'te--4st||'
        db.session.add(user)
        db.session.add(org)

        org.org_members.append(
            OrgMember(user=user, role=Roles.MEMBER.value)
        )
        db.session.commit()
        assert len(org.org_members) == 2

        rv = client.patch(
            f"v2/orgs/{org.uuid}/users/{user.uuid}",
            headers=myheaders(token_v2),
            json={'role': 'product'}
        )
        assert rv.status_code == 200

        rv = client.get(f"v2/orgs/{org.uuid}/users", headers=myheaders(token_v2))
        assert rv.status_code == 200
        data = rv.get_json()
        assert 'users' in data
        assert len(data['users']) == 2
        assert len([x for x in data['users'] if x['role'] == Roles.PRODUCT.value]) == 1


def test_remove_user_from_org(client, token_v2):
    with app.app_context():
        org = Org.query.first()
        cur_org_member = OrgMember.query.filter_by(
            user_id=org.org_members[0].user.id, org_id=org.id
        ).first()

        rv = client.delete(
            f"v2/orgs/1111111111/users/{org.org_members[0].user.uuid}",
            headers=myheaders(token_v2),
        )
        assert rv.status_code == 404

        rv = client.delete(
            f"v2/orgs/{org.uuid}/users/11111",
            headers=myheaders(token_v2),
        )
        assert rv.status_code == 404

        rv = client.delete(
            f"v2/orgs/{org.uuid}/users/{org.org_members[0].user.uuid}",
            headers=myheaders(token_v2),
        )
        assert rv.status_code == 422
        assert b'yourself' in rv.data

        user = User()
        user.username = 'Member 1'
        user.email = 'member@test.com'
        user.password = 'te--4st||'
        db.session.add(user)
        db.session.commit()
        rv = client.delete(
            f"v2/orgs/{org.uuid}/users/{user.uuid}",
            headers=myheaders(token_v2),
        )
        assert rv.status_code == 422
        assert b'not in' in rv.data

        org.org_members.append(
            OrgMember(user=user, role=Roles.MEMBER.value)
        )
        db.session.commit()
        assert len(org.org_members) == 2

        cur_org_member.role = Roles.MEMBER.value
        db.session.commit()
        rv = client.delete(
            f"v2/orgs/{org.uuid}/users/{user.uuid}",
            headers=myheaders(token_v2),
        )
        assert rv.status_code == 403

        cur_org_member.role = Roles.OWNER.value
        db.session.commit()
        org_uuid = org.uuid
        user2_uuid = user.uuid

    client.delete(
        f"v2/orgs/{org_uuid}/users/{user2_uuid}",
        headers=myheaders(token_v2),
    )
    rv = client.get(f"v2/orgs/{org_uuid}/users", headers=myheaders(token_v2))
    assert rv.status_code == 200
    assert 'users' in rv.get_json()
    assert len(rv.get_json()['users']) == 1


def test_default_org(client, app_context, token_v2):
    org1 = Org()
    org1.name = "Axios"
    org1.home_country = 'FR'
    org1.setup_new_org()
    db.session.add(org1)

    # Now put a user into the Org and give them the default zone
    user1 = User.query.filter_by(email="scooter3@example.com").first()
    db.session.add(user1)

    org1.org_members.append(OrgMember(user=user1, role="owner"))
    db.session.commit()

    assert len(org1.zones) == 1  # default zone was created for us
    assert Org.query.filter_by(id=user1.default_org_id).first() is not None

    # Add user to another Org
    org2 = Org()
    org2.name = "Axios2"
    org2.home_country = 'FR'
    org2.setup_new_org()
    db.session.add(org2)

    # make user a member of the org
    org2.org_members.append(OrgMember(user=user1, role="member"))
    db.session.commit()

    # Set new org as their default Org
    user1.default_org_id = org2.id
    db.session.commit()

    # Make sure /v2/me works
    rv = client.get("/v2/me", headers=myheaders(token_v2))
    assert rv.status_code == 200
    org2_uuid = '' + org2.uuid
    assert rv.get_json()['default_org'] == org2_uuid

    # Now delete Org2 and make sure that User's default org falls back to another org
    org2.soft_delete()
    db.session.commit()

    rv = client.get("/v2/me", headers=myheaders(token_v2))
    assert rv.status_code == 200
    assert rv.get_json()['default_org'] != org2_uuid


def test_roles_notifications(client, token_v2):
    with app.app_context():
        org = Org.query.first()

        user = User()
        user.username = 'Member 1'
        user.email = 'member@test.com'
        user.password = 'te--4st||'
        db.session.add(user)

        notif = Notifications(role='product', text='test text test')
        db.session.add(notif)

        org.org_members.append(OrgMember(user=user, role=Roles.PRODUCT.value))
        db.session.commit()

        rv = client.get(
            f"v2/orgs/{org.uuid}/users/{user.uuid}/notifications",
            headers=myheaders(token_v2)
        )
        assert rv.status_code == 200
        data = rv.get_json()
        notifications = data['notifications']
        assert len(notifications) == 1
        assert not notifications[0]['value']
        new_notification_id = notifications[0]['id']

        rv = client.post(
            f"v2/orgs/{org.uuid}/users/{user.uuid}/notifications",
            headers=myheaders(token_v2),
            json={'notifications': [new_notification_id]}
        )
        assert rv.status_code == 200

        rv = client.get(
            f"v2/orgs/{org.uuid}/users/{user.uuid}/notifications",
            headers=myheaders(token_v2)
        )
        assert rv.status_code == 200
        data = rv.get_json()
        notifications = data['notifications']
        assert len(notifications) == 1
        assert notifications[0]['value']

        rv = client.post(
            f"v2/orgs/{org.uuid}/users/{user.uuid}/notifications",
            headers=myheaders(token_v2),
            json={'notifications': []}
        )
        assert rv.status_code == 200

        rv = client.get(
            f"v2/orgs/{org.uuid}/users/{user.uuid}/notifications",
            headers=myheaders(token_v2)
        )
        assert rv.status_code == 200
        data = rv.get_json()
        notifications = data['notifications']
        assert len(notifications) == 1
        assert not notifications[0]['value']


def test_create_org_schema(client, token_v2):
    # Create org first
    rv = client.post(
        "/v2/orgs",
        json={"name": "ACME org", "country": "RU"},
        headers=myheaders(token_v2),
    )
    org_id = rv.get_json()['id']
    assert org_id is not None

    rv = client.post(f"/v2/orgs/{org_id}/schemas", json={}, headers=myheaders(token_v2))
    assert rv.status_code == 400  # missing name

    rv = client.post(f"/v2/orgs/{org_id}/schemas", json={"name": ""}, headers=myheaders(token_v2))
    assert rv.status_code == 400  # empty name

    rv = client.post(f"/v2/orgs/{org_id}/schemas", json={"name": "acme_schema"}, headers=myheaders(token_v2))
    assert rv.status_code == 200

    data = rv.get_json()

    assert 'id' in data
    assert 'name' in data

    rv = client.post(f"/v2/orgs/{org_id}/schemas", json={"name": "acme_schema"}, headers=myheaders(token_v2))
    assert rv.status_code == 400  # duplicate schema


def test_get_org_schema(client, token_v2):
    with app.app_context():
        org = Org.query.first()

        # Create schema first
        rv = client.post(f"/v2/orgs/{org.uuid}/schemas", json={"name": "acme_schema"}, headers=myheaders(token_v2))
        schema_id = rv.get_json()['id']
        assert schema_id is not None

        # Get created schema
        rv = client.get(f"/v2/orgs/{org.uuid}/schemas/{schema_id}", headers=myheaders(token_v2))
        assert rv.status_code == 200

        data = rv.get_json()

        assert 'id' in data
        assert data['id'] == schema_id


def test_get_org_schemas(client, token_v2):
    with app.app_context():
        org = Org.query.first()

        # Create schemas
        rv = client.post(
            f"/v2/orgs/{org.uuid}/schemas", json={"name": "acme_schema1_for_list_test"}, headers=myheaders(token_v2)
        )
        schema_1_id = rv.get_json()['id']
        assert schema_1_id is not None

        rv = client.post(
            f"/v2/orgs/{org.uuid}/schemas", json={"name": "acme_schema2_for_list_test"}, headers=myheaders(token_v2)
        )
        schema_2_id = rv.get_json()['id']
        assert schema_2_id is not None

        # Get created schema
        rv = client.get(f"/v2/orgs/{org.uuid}/schemas", headers=myheaders(token_v2))
        assert rv.status_code == 200

        schemas = rv.get_json()

        assert len(schemas) == 2

        for schema in schemas:
            assert 'id' in schema
            assert 'name' in schema
            assert schema['id'] == schema_1_id or schema['id'] == schema_2_id


def test_create_org_schema_table(client, token_v2):
    with app.app_context():
        org = Org.query.first()

        # Create schema
        rv = client.post(
            f"/v2/orgs/{org.uuid}/schemas", json={"name": "acme_schema_for_table_test"}, headers=myheaders(token_v2)
        )
        schema_id = rv.get_json()['id']
        assert schema_id is not None

        rv = client.post(
            f"/v2/orgs/{org.uuid}/schemas/{schema_id}/tables", json={}, headers=myheaders(token_v2)
        )
        assert rv.status_code == 400

        rv = client.post(
            f"/v2/orgs/{org.uuid}/schemas/{schema_id}/tables", json={"name": ""}, headers=myheaders(token_v2)
        )
        assert rv.status_code == 400

        rv = client.post(
            f"/v2/orgs/{org.uuid}/schemas/{schema_id}/tables", json={"name": "acme_table"}, headers=myheaders(token_v2)
        )
        assert rv.status_code == 200

        data = rv.get_json()

        assert 'id' in data
        assert 'name' in data

        rv = client.post(
            f"/v2/orgs/{org.uuid}/schemas/{schema_id}/tables", json={"name": "acme_table"}, headers=myheaders(token_v2)
        )
        assert rv.status_code == 400


def test_create_org_schema_column(client, token_v2):
    with app.app_context():
        org = Org.query.first()

        # Create schema
        rv = client.post(
            f"/v2/orgs/{org.uuid}/schemas", json={"name": "acme_schema_for_column_test"}, headers=myheaders(token_v2)
        )
        schema_id = rv.get_json()['id']
        assert schema_id is not None

        # Create table
        rv = client.post(
            f"/v2/orgs/{org.uuid}/schemas/{schema_id}/tables",
            json={"name": "acme_table_for_column_test"},
            headers=myheaders(token_v2)
        )
        table_id = rv.get_json()['id']
        assert table_id is not None

        rv = client.post(
            f"/v2/orgs/{org.uuid}/schemas/{schema_id}/tables/{table_id}/columns",
            json={},
            headers=myheaders(token_v2)
        )
        assert rv.status_code == 400

        # Not all required fields
        rv = client.post(
            f"/v2/orgs/{org.uuid}/schemas/{schema_id}/tables/{table_id}/columns",
            json={"name": "acme_column"},
            headers=myheaders(token_v2)
        )
        assert rv.status_code == 400

        rv = client.post(
            f"/v2/orgs/{org.uuid}/schemas/{schema_id}/tables/{table_id}/columns",
            json={"name": "acme_column", "type": OrgSchemaTableColumn.TYPE_SHORT_STRING},
            headers=myheaders(token_v2)
        )
        assert rv.status_code == 400

        rv = client.post(
            f"/v2/orgs/{org.uuid}/schemas/{schema_id}/tables/{table_id}/columns",
            json={
                "name": "acme_column",
                "type": OrgSchemaTableColumn.TYPE_SHORT_STRING,
                "privacy_strategy": OrgSchemaTableColumn.PRIVACY_STRATEGY_HASH,
            },
            headers=myheaders(token_v2)
        )
        assert rv.status_code == 400

        # Bad privacy_strategy
        rv = client.post(
            f"/v2/orgs/{org.uuid}/schemas/{schema_id}/tables/{table_id}/columns",
            json={
                "name": "acme_column",
                "type": OrgSchemaTableColumn.TYPE_SHORT_STRING,
                "privacy_strategy": "bullshit",
                "default_value": "123",
            },
            headers=myheaders(token_v2)
        )
        assert rv.status_code == 400

        # Bad type
        rv = client.post(
            f"/v2/orgs/{org.uuid}/schemas/{schema_id}/tables/{table_id}/columns",
            json={
                "name": "acme_column",
                "type": "bullshit",
                "privacy_strategy": OrgSchemaTableColumn.PRIVACY_STRATEGY_HASH,
                "default_value": "123",
            },
            headers=myheaders(token_v2)
        )
        assert rv.status_code == 400

        rv = client.post(
            f"/v2/orgs/{org.uuid}/schemas/{schema_id}/tables/{table_id}/columns",
            json={
                "name": "acme_column",
                "type": OrgSchemaTableColumn.TYPE_SHORT_STRING,
                "privacy_strategy": OrgSchemaTableColumn.PRIVACY_STRATEGY_HASH,
                "default_value": "123",
            },
            headers=myheaders(token_v2)
        )
        assert rv.status_code == 200

        data = rv.get_json()

        assert 'id' in data
        assert 'name' in data

        # duplicate column
        rv = client.post(
            f"/v2/orgs/{org.uuid}/schemas/{schema_id}/tables/{table_id}/columns",
            json={
                "name": "acme_column",
                "type": OrgSchemaTableColumn.TYPE_SHORT_STRING,
                "privacy_strategy": OrgSchemaTableColumn.PRIVACY_STRATEGY_HASH,
                "default_value": "ggg",
            },
            headers=myheaders(token_v2)
        )
        assert rv.status_code == 400


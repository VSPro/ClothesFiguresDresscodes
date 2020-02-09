import datetime

from portalbackend import app
from portalbackend.models import Zone
from .conftest import myheaders


def test_create_zone(client, token_v2):
    # Create org first
    rv = client.post(
        "/v2/orgs",
        json={"name": "ACME org", "country": "US"},
        headers=myheaders(token_v2),
    )
    org_id = rv.get_json()['id']

    rv = client.post(
        f"/v2/orgs/{org_id}/zones",
        headers=myheaders(token_v2),
        json={
            "name": "Production",
            "label": "Test label",
        },
    )
    assert rv.status_code == 200
    data = rv.get_json()
    assert 'id' in data
    assert 'name' in data
    assert 'label' in data
    assert data['name'] == 'Production'
    assert data['label'] == 'Test label'

    real_limit = app.config.get('LIMIT_ZONES')
    app.config['LIMIT_ZONES'] = 1
    rv = client.post(
        f"/v2/orgs/{org_id}/zones",
        headers=myheaders(token_v2),
        json={
            "name": "Limited zones",
            "label": "Test label",
        },
    )
    assert rv.status_code == 403
    app.config['LIMIT_ZONES'] = real_limit

    rv = client.post(
        f"/v2/orgs/1111/zones",
        headers=myheaders(token_v2),
        json={
            "name": "Production",
            "label": "Test label",
        },
    )
    assert rv.status_code == 404

    rv = client.post(
        f"/v2/orgs/{org_id}/zones",
        headers=myheaders(token_v2),
        json={},
    )

    assert rv.status_code == 422


def test_get_zones(client, token_v2):
    rv = client.post(
        "/v2/orgs", json={"name": "IBM Co", "country": "US"},
        headers=myheaders(token_v2))
    assert rv.status_code == 200

    org_id = rv.get_json()['id']
    assert org_id is not None

    path = f"/v2/orgs/{org_id}/zones"
    rv = client.get(path, headers=myheaders(token_v2))
    assert rv.status_code == 200
    zones = rv.get_json()
    assert len(zones) > 0
    assert 'id' in zones[0]
    assert 'api_keys' in zones[0]
    assert 'label' in zones[0]['api_keys'][0]
    assert 'prefix' in zones[0]['api_keys'][0]


def test_update_zone(client, token_v2):
    with app.app_context():
        zone = Zone.query.first()
        rv = client.patch(
            f"/v2/zones/{zone.uuid}",
            headers=myheaders(token_v2),
        )
        assert rv.status_code == 400

        rv = client.patch(
            f"/v2/zones/2222",
            headers=myheaders(token_v2),
            json={"name": "Staging"}
        )
        assert rv.status_code == 404

        rv = client.patch(
            f"/v2/zones/{zone.uuid}",
            headers=myheaders(token_v2),
            json={"name": "Staging"}
        )
        assert rv.status_code == 200
        rev_zone = Zone.query.filter_by(uuid=zone.uuid).first()
        assert rev_zone.name == 'Staging'


def test_delete_zone(client, token_v2):
    with app.app_context():
        zone_id = Zone.query.first().uuid
    rv = client.post(
        f"/v2/zones/{zone_id}/apikeys",
        headers=myheaders(token_v2),
        json={}
    )
    with app.app_context():
        zone = Zone.query.filter_by(uuid=zone_id).first()
        assert len(zone.api_keys) == 2
    rv = client.delete(
        f"/v2/zones/{zone_id}",
        headers=myheaders(token_v2),
    )
    assert rv.status_code == 200
    with app.app_context():
        assert Zone.query.filter_by(uuid=zone_id).scalar() is None

    rv = client.delete(
        f"/v2/zones/1111",
        headers=myheaders(token_v2),
    )
    assert rv.status_code == 404
    with app.app_context():
        rev_zone = (
            Zone.query.filter_by(uuid=zone_id)
                .execution_options(include_deleted=True)
                .first()
        )
        assert len(rev_zone.api_keys) == 0
    assert rev_zone.deleted is True
    assert rev_zone.deleted_at.date() == datetime.datetime.utcnow().date()

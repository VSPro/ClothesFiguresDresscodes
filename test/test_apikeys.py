import datetime
import json

import pytest

from portalbackend import db, app
from portalbackend.models import Zone, ZoneAPIKey
from portalbackend.orgs.models import Org
from .conftest import myheaders


@pytest.fixture
def org_2(client):
    org2 = Org(name="Google", home_country="US")
    zone_2 = Zone()
    org2.zones.append(zone_2)
    db.session.add(org2)
    db.session.commit()
    yield org2


def test_api_key_wrong_param_name(client, token_v2, app_context):
    wrong_parameter_name = "prefix"

    zone_id = Zone.query.first().uuid

    rv = client.post(
        f"/v2/zones/{zone_id}/apikeys",
        json={wrong_parameter_name: "whatever"},
        headers=myheaders(token_v2),
    )
    assert rv.status_code == 400

    error = json.loads(rv.data.decode())["errors"][0]
    assert error["code"] == "ERR_VALIDATION"
    assert error["source"] == "{'prefix': ['Unknown field.']}"


@pytest.fixture
def change_api_key_limit_option():
    limit, app.config["LIMIT_API_KEYS"] = app.config["LIMIT_API_KEYS"], 1
    yield
    app.config["LIMIT_API_KEYS"] = limit


def test_api_key_limit_option(
    client, token_v2, app_context, change_api_key_limit_option
):
    zone_id = Zone.query.first().uuid
    rv = client.post(
        f"/v2/zones/{zone_id}/apikeys",
        json={},
        headers=myheaders(token_v2),
    )
    assert rv.status_code == 403

    error = json.loads(rv.data.decode())["errors"][0]
    assert error["code"] == "ERR_TENANT"
    assert "API keys limit exceed for zone" in error["detail"]


def test_api_key_content(client, token_v2, app_context):
    zone_id = Zone.query.first().uuid
    rv = client.post(
        f"/v2/zones/{zone_id}/apikeys",
        json={},
        headers=myheaders(token_v2),
    )
    assert rv.status_code == 200

    api_key = rv.get_json()

    assert isinstance(api_key, dict)
    assert "api_key" in api_key
    assert "prefix" in api_key
    assert "composite_id" in api_key

    assert len(api_key["api_key"]) == 32


def test_get_apikeys(client, token_v2, app_context, org_2):
    zone_id = Zone.query.first().uuid
    rv = client.get(f"/v2/zones/{zone_id}/apikeys", headers=myheaders(token_v2))
    assert rv.status_code == 200
    resp = rv.get_json()
    assert type(resp) is dict
    assert "api_keys" in resp
    apikeys = resp["api_keys"]
    assert len(apikeys) >= 1
    assert "label" in apikeys[0]
    assert "prefix" in apikeys[0]
    assert "api_key" in apikeys[0]

    db.session.add(org_2)
    zone_id = org_2.zones[0].uuid
    rv = client.get(f"/v2/zones/{zone_id}/apikeys", headers=myheaders(token_v2))
    assert rv.status_code == 403


def test_update_apikey(client, token_v2, app_context, org_2):
    zone = Zone.query.first()
    zone_id = zone.uuid
    apikey_id = zone.api_keys[0].uuid
    rv = client.put(
        f"/v2/zones/{zone_id}/apikeys/{apikey_id}",
        headers=myheaders(token_v2),
        json={}
    )
    assert rv.status_code == 404
    assert b"No fields" in rv.data

    rv = client.put(
        f"/v2/zones/{zone_id}/apikeys/{apikey_id}",
        headers=myheaders(token_v2),
        json={"label": "my_first_label"},
    )
    assert rv.status_code == 200
    rel_apikey = ZoneAPIKey.query.filter_by(uuid=apikey_id).one()
    assert rel_apikey.label == "my_first_label"

    rv = client.put(
        f"/v2/zones/{zone_id}/apikeys/{apikey_id}",
        headers=myheaders(token_v2),
        json={"label": "my_second_label", "store_plain": "False"},
    )
    assert rv.status_code == 200
    rel_apikey = ZoneAPIKey.query.filter_by(uuid=apikey_id).one()
    assert rel_apikey.label == "my_second_label"
    assert rel_apikey.store_plain is False
    assert rel_apikey.api_key_plain is None
    assert rel_apikey._api_key and len(rel_apikey._api_key) > 0

    rv = client.put(
        f"/v2/zones/{zone_id}/apikeys/{apikey_id}",
        headers=myheaders(token_v2),
        json={"prefix": "glsmto"},
    )
    assert rv.status_code == 422
    assert b"prefix" in rv.data

    rv = client.put(
        f"/v2/zones/{zone_id}/apikeys/{apikey_id}",
        headers=myheaders(token_v2),
        json={"store_plain": "True"},
    )
    assert rv.status_code == 412
    assert b"Unable to recover removed" in rv.data

    db.session.add(org_2)
    zone = org_2.zones[0]
    zone_id = zone.uuid
    apikey_id = zone.api_keys[0].uuid
    rv = client.put(
        f"/v2/zones/{zone_id}/apikeys/{apikey_id}",
        headers=myheaders(token_v2),
        json={"label": "test_label"},
    )
    assert rv.status_code == 403


def test_soft_delete_api_key(client, token_v2):
    with app.app_context():
        zoneapikey = ZoneAPIKey.query.first()
        zoneapikey_id = zoneapikey.uuid
        zoneapikey_prefix = zoneapikey.prefix
        zone_id = zoneapikey.zone.uuid

    assert app._consul._confirm_key_registered_v3(zone_id, zoneapikey_prefix)
    rv = client.delete(
        f"/v2/zones/sjnvzxmnc/apikeys/{zoneapikey_id}", headers=myheaders(token_v2)
    )
    rv.status_code == 404
    rv = client.delete(
        f"/v2/zones/{zone_id}/apikeys/kjasdfkjafds", headers=myheaders(token_v2)
    )
    rv.status_code == 404
    rv = client.delete(
        f"/v2/zones/{zone_id}/apikeys/{zoneapikey_id}", headers=myheaders(token_v2)
    )
    rv.status_code == 200
    assert app._consul._confirm_key_registered_v3(zone_id, zoneapikey_prefix) is False
    with app.app_context():
        rev_apikey = (
            ZoneAPIKey.query.filter_by(uuid=zoneapikey_id)
            .execution_options(include_deleted=True)
            .first()
        )
    assert rev_apikey.deleted is True
    assert rev_apikey.deleted_at.date() == datetime.datetime.utcnow().date()

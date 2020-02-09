# Fixtures
from datetime import datetime, timedelta

from portalbackend import db
from portalbackend.models import UsageSummary, Zone, UsageTotals
from test.conftest import myheaders

HOURLY = UsageSummary.INTERVAL_HOURLY


def test_basic_usage(client, app_context):
    tsnow = UsageSummary.align_ts(datetime.utcnow(), HOURLY)

    usage = UsageSummary(
        zone_id=1, country='us',
        interval=UsageSummary.INTERVAL_HOURLY,
        timestamp=tsnow,
        total_inserts=1,
        total_reads=2,
        total_writes=3,
        total_errors=4,
        total_bandwidth=100)

    db.session.add(usage)
    db.session.commit()

    u2 = UsageSummary.query.filter_by(zone_id=1, country='us', interval=HOURLY, timestamp=tsnow).first()
    assert u2 is not None

    assert u2.total_inserts == 1
    assert u2.total_reads == 2
    assert u2.total_writes == 3
    assert u2.total_errors == 4
    assert u2.total_bandwidth == 100

    # Add some data
    UsageSummary.record_usage(zone=1, country='us', timestamp=tsnow, interval=HOURLY,
                              inserts=10, reads=20)

    UsageSummary.record_usage(zone=1, country='us', timestamp=tsnow, interval=HOURLY,
                              writes=30, errors=40, bandwidth=50)

    u3 = UsageSummary.query.filter_by(zone_id=1, country='us', interval=HOURLY, timestamp=tsnow).first()

    assert u3.total_inserts == (1 + 10)
    assert u3.total_reads == (2 + 20)
    assert u3.total_writes == (3 + 30)
    assert u3.total_errors == (4 + 40)
    assert u3.total_bandwidth == (100 + 50)


def test_usage_events(client, app_context):
    headers = {"Authorization": "Bearer marc_secret"}
    rv = client.post("/v2/usage/events", json=[])
    assert rv.status_code == 401

    rv = client.post("/v2/usage/events", json=[], headers=headers)
    assert rv.status_code == 200

    # 3 reads, 1 insert, 2 updates, 1 error, 10*5 bandwidth
    testnow = datetime.utcnow()
    events = [
        {"zone_id": 2, "country": "de", "http_verb": "GET", "path": "/", "status_code": 200, "bandwidth": 10,
         "new_record": False, "timestamp": datetime.utcnow().isoformat()},
        {"zone_id": 2, "country": "de", "http_verb": "GET", "path": "/", "status_code": 200, "bandwidth": 10,
         "new_record": False, "timestamp": datetime.utcnow().isoformat()},
        {"zone_id": 2, "country": "de", "http_verb": "GET", "path": "/", "status_code": 200, "bandwidth": 10,
         "new_record": False, "timestamp": datetime.utcnow().isoformat()},
        {"zone_id": 2, "country": "de", "http_verb": "POST", "path": "/", "status_code": 200, "bandwidth": 10,
         "new_record": True, "timestamp": datetime.utcnow().isoformat()},
        {"zone_id": 2, "country": "de", "http_verb": "POST", "path": "/", "status_code": 200, "bandwidth": 10,
         "new_record": False, "timestamp": datetime.utcnow().isoformat()},
        {"zone_id": 2, "country": "de", "http_verb": "POST", "path": "/", "status_code": 500, "bandwidth": 10,
         "new_record": False, "timestamp": datetime.utcnow().isoformat()},
        {"zone_id": 2, "country": "de", "http_verb": "POST", "path": "/delete", "status_code": 200, "bandwidth": 0,
         "new_record": False, "timestamp": datetime.utcnow().isoformat()},
    ]

    rv = client.post("/v2/usage/events", json=events, headers=headers)
    assert rv.status_code == 200

    usage = UsageSummary.query.filter_by(zone_id=2, country='de',
                                         interval=UsageSummary.INTERVAL_HOURLY,
                                         timestamp=UsageSummary.align_ts(testnow, UsageSummary.INTERVAL_HOURLY)).first()
    assert usage is not None

    assert usage.total_reads == 3
    assert usage.total_inserts == 0
    assert usage.total_writes == 4
    assert usage.total_errors == 1
    assert usage.total_bandwidth == (10 * 6)

    # Stuff some data for an hour from now
    testnow2 = datetime.utcnow() + timedelta(hours=1)
    events2 = [
        {"zone_id": 2, "country": "de", "http_verb": "GET", "path": "/", "status_code": 200, "bandwidth": 10,
         "new_record": False, "timestamp": testnow2.isoformat()},
    ]
    rv = client.post("/v2/usage/events", json=events2, headers=headers)
    assert rv.status_code == 200

    # Verify the old record didn't change
    db.session.expire_all()
    usage = UsageSummary.query.filter_by(zone_id=2, country='de',
                                         interval=UsageSummary.INTERVAL_HOURLY,
                                         timestamp=UsageSummary.align_ts(testnow, UsageSummary.INTERVAL_HOURLY)).first()

    assert usage.total_reads == 3
    assert usage.total_bandwidth == (10 * 6)

    # And verify we got a new usage record
    u2 = UsageSummary.query.filter_by(zone_id=2, country='de',
                                      interval=UsageSummary.INTERVAL_HOURLY,
                                      timestamp=UsageSummary.align_ts(testnow2, UsageSummary.INTERVAL_HOURLY)).first()
    assert u2 is not None
    assert u2.total_reads == 1
    assert u2.total_bandwidth == 10


def test_usage_totals(client, token_v2, app_context):
    headers = {"Authorization": "Bearer marc_secret"}
    rv = client.post("/v2/usage/totals")
    assert rv.status_code == 401

    rv = client.post("/v2/usage/totals", json={}, headers=headers)
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['count'] == 0

    rv = client.post(
        "/v2/orgs",
        json={"name": "ACME org", "country": "US"},
        headers=myheaders(token_v2),
    )
    data = rv.get_json()
    org_id = data['id']

    rv = client.post(
        f"/v2/orgs/{org_id}/zones",
        headers=myheaders(token_v2),
        json={"name": "Production"},
    )
    data = rv.get_json()
    zone_1_uuid = data['id']

    rv = client.post(
        f"/v2/orgs/{org_id}/zones",
        headers=myheaders(token_v2),
        json={"name": "Staging"},
    )
    data = rv.get_json()
    zone_2_uuid = data['id']

    zone_id_by_uuid = {
        x[1]: x[0] for x in db.session.query(
            Zone.id,
            Zone.uuid
        ).filter(
            Zone.uuid.in_([zone_1_uuid, zone_2_uuid])
        )
    }

    testnow = datetime.utcnow()
    events = [
        {"zone_id": zone_id_by_uuid[zone_1_uuid], "country": "fr", "http_verb": "GET",
         "path": "/", "status_code": 200, "bandwidth": 10,
         "new_record": False, "timestamp": datetime.utcnow().isoformat()},
        {"zone_id": zone_id_by_uuid[zone_1_uuid], "country": "fr", "http_verb": "GET",
         "path": "/", "status_code": 200, "bandwidth": 10,
         "new_record": False, "timestamp": datetime.utcnow().isoformat()},
        {"zone_id": zone_id_by_uuid[zone_1_uuid], "country": "fr", "http_verb": "GET",
         "path": "/", "status_code": 200, "bandwidth": 10,
         "new_record": False, "timestamp": datetime.utcnow().isoformat()},
        {"zone_id": zone_id_by_uuid[zone_2_uuid], "country": "en", "http_verb": "GET",
         "path": "/", "status_code": 200, "bandwidth": 10,
         "new_record": False, "timestamp": datetime.utcnow().isoformat()},
        {"zone_id": zone_id_by_uuid[zone_2_uuid], "country": "en", "http_verb": "POST",
         "path": "/", "status_code": 200, "bandwidth": 10,
         "new_record": True, "timestamp": datetime.utcnow().isoformat()},
        {"zone_id": zone_id_by_uuid[zone_2_uuid], "country": "en", "http_verb": "POST",
         "path": "/", "status_code": 200, "bandwidth": 10,
         "new_record": False, "timestamp": datetime.utcnow().isoformat()},
        {"zone_id": zone_id_by_uuid[zone_2_uuid], "country": "en", "http_verb": "POST",
         "path": "/", "status_code": 500, "bandwidth": 10,
         "new_record": False, "timestamp": datetime.utcnow().isoformat()},
        {"zone_id": zone_id_by_uuid[zone_2_uuid], "country": "en", "http_verb": "POST",
         "path": "/delete", "status_code": 200, "bandwidth": 0,
         "new_record": False, "timestamp": datetime.utcnow().isoformat()},
    ]

    rv = client.post("/v2/usage/events", json=events, headers=headers)
    assert rv.status_code == 200

    totals = [
        {"zone_id": zone_id_by_uuid[zone_1_uuid], "country": "fr", "rows": 100},
        {"zone_id": zone_id_by_uuid[zone_2_uuid], "country": "en", "rows": 50},
    ]

    rv = client.post("/v2/usage/totals", json={'totals': totals}, headers=headers)
    assert rv.status_code == 200

    usage = UsageSummary.query.filter_by(
        zone_id=zone_id_by_uuid[zone_1_uuid], country='fr',
        interval=UsageSummary.INTERVAL_HOURLY,
        timestamp=UsageSummary.align_ts(testnow, UsageSummary.INTERVAL_HOURLY)
    ).first()
    assert usage is not None
    assert usage.total_reads == 3
    assert usage.total_inserts == 0
    assert usage.total_writes == 0
    assert usage.total_errors == 0
    assert usage.total_bandwidth == (10 * 3)

    usage = UsageSummary.query.filter_by(
        zone_id=zone_id_by_uuid[zone_2_uuid], country='en',
        interval=UsageSummary.INTERVAL_HOURLY,
        timestamp=UsageSummary.align_ts(testnow, UsageSummary.INTERVAL_HOURLY)
    ).first()
    assert usage is not None
    assert usage.total_reads == 1
    assert usage.total_inserts == 0
    assert usage.total_writes == 4
    assert usage.total_errors == 1
    assert usage.total_bandwidth == (10 * 4)

    usage = UsageTotals.query.filter_by(
        zone_id=zone_id_by_uuid[zone_1_uuid], country='fr',
    ).first()
    assert usage is not None
    assert usage.totals == 100

    usage = UsageTotals.query.filter_by(
        zone_id=zone_id_by_uuid[zone_2_uuid], country='en',
    ).first()
    assert usage is not None
    assert usage.totals == 50

    rv = client.get(
        f"/v2/usage/report",
        headers=myheaders(token_v2)
    )
    data = rv.get_json()
    assert 'details' in data
    assert 'summary' in data
    assert len(data['details']) == 2
    assert 'rows' in data['details'][0]
    assert len(data['details'][0]['rows']) == 1
    assert len(data['summary']) == 2
    assert all(k in data['summary'][0] for k in (
        'bandwidth', 'country', 'errors', 'inserts', 'reads',
        'total_rows', 'writes', 'zone_uuid'))

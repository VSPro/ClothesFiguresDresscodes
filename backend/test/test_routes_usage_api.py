import random
from datetime import datetime, timedelta

# TODO maybe mocks instead?
from faker import Faker

from portalbackend import db
from portalbackend.models import UsageSummary, Zone
from .conftest import myheaders


def test_usage_api(client, token_v2, app_context):
    fake = Faker()
    country1 = fake.country_code()
    country2 = fake.country_code()
    zone = Zone.query.first()
    usages = []
    for country in [country1, country2]:
        for _ in range(6):
            timestamp = fake.date_time_between(
                start_date='-30d', end_date='now'
            )
            inserts = random.randint(100, 10000)
            usage = UsageSummary(
                zone_id=zone.id,
                country=country,
                timestamp=timestamp,
                total_inserts=inserts,
                total_reads=random.randint(0, inserts),
                total_writes=random.randint(0, inserts),
                total_errors=random.randint(0, inserts//10),
                total_bandwidth=inserts,
            )
            usages.append(usage)
    db.session.bulk_save_objects(usages)
    db.session.commit()

    zone_id = zone.uuid
    end_dt = datetime.now()
    end = end_dt.strftime('%Y-%d-%m-%H:%M')
    _30days = timedelta(weeks=4) + timedelta(days=2)
    start = (end_dt - _30days).strftime('%Y-%d-%m-%H:%M')
    rv = client.get(
        f"/v2/usage/hourly?zone_id={zone_id}&start={start}&end={end}",
        headers=myheaders(token_v2),
    )
    assert rv.status_code == 200
    usage_sum = rv.get_json()
    assert 'events' in usage_sum
    events = usage_sum['events']
    assert type(events) is list
    assert len(events) == 12
    assert events[0]["country"] == country1 or country2
    assert 'rows' in events[0]
    for item, _ in events[0]['rows'][0].items():
        assert item in ['bandwidth', 'timestamp', 'reads', 'writes', 'errors', 'inserts']

    rv = client.get(
        f"/v2/usage/daily?zone_id={zone_id}&start={start}&end={end}",
        headers=myheaders(token_v2),
    )
    assert rv.status_code == 200
    assert 'events' in rv.get_json()

    rv = client.get(
        f"/v2/usage/hourly?zone_id={111}&start={start}&end={end}",
        headers=myheaders(token_v2),
    )
    assert rv.status_code == 404

    rv = client.get(
        f"/v2/usage/hourly?zone_id={zone_id}&start=some_date&end={end}",
        headers=myheaders(token_v2),
    )
    assert rv.status_code == 422

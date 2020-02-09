# Fixtures
from portalbackend import db
from portalbackend.models import User, Zone, ZoneAPIKey
from portalbackend.orgs.models import Org, OrgMember


def test_orgs(client, app_context):
    org1 = Org()
    org1.name = "Apple Inc."
    org1.home_country = 'US'
    zone1 = Zone(name='test env')
    org1.zones.append(zone1)

    db.session.add(org1)
    db.session.add(zone1)
    db.session.commit()

    assert org1.uuid is not None
    assert zone1.uuid is not None

    reloaded = Org.query.filter_by(uuid=org1.uuid).first()
    assert reloaded is not None
    assert reloaded.name == org1.name
    assert len(reloaded.zones) == 1


def test_members(client, app_context):
    org1 = Org()
    org1.name = "Apple Inc."
    org1.home_country = 'US'

    user1 = User(
        username='Owner 1',
        email='owner@test.com',
        password='te--4st||'
    )
    user2 = User(
        username='Member 1',
        email='member@test.com',
        password='te--4st||'
    )

    org1.org_members.append(OrgMember(user=user1, role="owner"))
    org1.org_members.append(OrgMember(user=user2, role="member"))

    db.session.add(org1)
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    reloaded = Org.query.filter_by(uuid=org1.uuid).first()
    assert len(reloaded.org_members) == 2
    assert reloaded.org_members[0].user.uuid in [user1.uuid, user2.uuid]

    reluser1 = User.query.filter_by(uuid=user1.uuid).first()
    assert reluser1.orgs[0] == org1
    assert reluser1.memberships[0].role == 'owner'

    reluser2 = User.query.filter_by(uuid=user2.uuid).first()
    assert reluser2.orgs[0] == org1
    assert reluser2.memberships[0].role == 'member'

    # Now the money shot. Link a User to another Org
    org2 = Org(name="Pixar", home_country='CA')
    org2.org_members.append(OrgMember(user=user2, role="owner"))
    db.session.add(org2)
    db.session.commit()

    reluser3 = User.query.filter_by(uuid=user2.uuid).first()
    assert len(reluser3.orgs) == 2
    assert org2 in reluser3.orgs

    membership2 = next(membership for membership in reluser3.memberships if membership.org == org2)
    assert membership2.role == 'owner'


def test_zones(client, app_context):
    org1 = Org()
    org1.name = "Big Blue"
    org1.label = "test"
    org1.home_country = 'DE'
    org1.setup_new_org()
    org1.zones.append(Zone(name="production env"))
    db.session.add(org1)
    db.session.commit()

    reloaded = Org.query.filter_by(uuid=org1.uuid).first()
    assert len(reloaded.zones) == 2
    assert reloaded.zones[0].uuid is not None
    assert reloaded.zones[0].uuid != reloaded.zones[1].uuid
    assert reloaded.zones[0].name == 'test zone'
    assert reloaded.zones[1].label == 'test'

    org1.zones.remove(reloaded.zones[0])
    assert len(org1.zones) == 1


def test_default_org(client, app_context):
    org1 = Org()
    org1.name = "Axios"
    org1.home_country = 'FR'
    org1.setup_new_org()
    db.session.add(org1)

    # Now put a user into the Org and give them the default zone
    user1 = User()
    user1.username = 'Owner 1'
    user1.email = 'owner@test.com'
    user1.password = 'te--4st||'
    org1.org_members.append(OrgMember(user=user1, role="owner"))
    db.session.add(user1)
    db.session.commit()

    assert len(org1.zones) == 1  # default zone was created for us

    user1.set_default_org(db.session)

    reloaded = User.query.filter_by(uuid=user1.uuid).first()
    assert reloaded.default_org_id == org1.id


def test_zone_api_keys(client, app_context):
    org1 = Org()
    org1.name = "Apple"
    org1.home_country = 'US'
    db.session.add(org1)
    music_zone = Zone(name='Apple Music', org_id=org1.id)
    db.session.add(music_zone)
    org1.zones.append(music_zone)

    zn_api_key = ZoneAPIKey(music_zone)
    db.session.add(zn_api_key)
    db.session.commit()

    rel_zone = Zone.query.filter_by(id=music_zone.id).first()
    rel_zone_key = ZoneAPIKey.query.filter_by(id=zn_api_key.id).first()
    assert rel_zone_key.api_key != ''
    assert rel_zone_key.api_key_plain != rel_zone_key.api_key
    assert len(rel_zone.api_keys) == 2
    assert rel_zone_key.check_api_key('random_key') is False
    assert rel_zone_key.check_api_key(zn_api_key.api_key_plain) is True

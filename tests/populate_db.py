import datetime as dt
# imports models related to the contact
from models.contact_model import (
    Contact,
)
from models.email_model import (
    Email,
    Type as EmailType,
)

# imports models related to experiences
from models.experience_model import (
    Experience,
    Degree,
    Type as ExpType,
    Month,
)
from models.achievement_model import Achievement

# imports models related to skills
from models.tag_model import (
    Tag,
    TagType,
    TagStatusType,
)
from models.tag_item_model import TagItem
from models.skill_model import (
    Skill,
    Capability,
    SkillRecommendation,
    CapabilitySkillSuggestion
)
from models.skill_item_model import ContactSkill
from resources.skill_utils import (
    get_skill_id,
    get_contact_skill,
    make_skill,
)

# imports models related to the resume
from models.resume_model import ResumeSnapshot

# imports models related to the program and cycle
from models.program_model import Program
from models.program_contact_model import ProgramContact
from models.program_app_model import ProgramApp
from models.opportunity_model import Opportunity
from models.opportunity_app_model import OpportunityApp
from models.session_model import UserSession
from models.profile_model import (
    Profile,
    Race,
    ContactAddress,
    RoleChoice,
    ProgramsCompleted
)

from .data.contact_data import CONTACTS_DATABASE, EMAILS_DATABASE
from .data.program_data import PROGRAMS_DATABASE
from .data.skill_data import SKILLS_NAMES
from .data.experience_data import (
    EXPERIENCES_DATABASE,
    ACHIEVEMENTS_DATABASE
)
from .data.profile_data import (
    ADDRESSES,
    PROGRAMS_COMPLETED,
    RACE,
    ROLES,
    PROFILES_DATABASE
)

# creates billy's contact
billy = Contact(**{**CONTACTS_DATABASE['billy'], 'stage': 3})
billy.email_primary = Email(**{
    **EMAILS_DATABASE['billy'],
    'type': EmailType('Personal'),
})

# creates obama's contact
obama = Contact(**CONTACTS_DATABASE['obama'])
obama.email_primary = Email(**{
    **EMAILS_DATABASE['obama'],
    'type': EmailType('Work'),
})


# creates billy's profile records
billy_profile = Profile(**PROFILES_DATABASE['billy'])
billy.profile = billy_profile

billy_address = ContactAddress(**ADDRESSES['billy'])
billy_profile.addresses.append(billy_address)
billy.addresses.append(billy_address)

billy_race = Race(**RACE['billy'])
billy_profile.race = billy_race
billy.race = billy_race

billy_p_complete = ProgramsCompleted(**PROGRAMS_COMPLETED['billy'])
billy_profile.programs_completed = billy_p_complete

billy_roles = RoleChoice(**ROLES['billy'])
billy_profile.roles = billy_roles


# creates billy's user session
billy_session = UserSession(
    id=123,
    auth_id='test-valid|0123456789abcdefabcdefff',
    contact_id=123,
    jwt='test_jwt',
    expiration=dt.datetime.utcnow(),
)


# creates obama's portfolio experience
obama_portfolio = Experience(**{
    **EXPERIENCES_DATABASE['obama_portfolio'],
    'start_month': Month('September'),
    'type': ExpType('Accomplishment'),
    'end_month': Month('May'),
})
obama.experiences.append(obama_portfolio)


# creates billy's educational experience
billy_edu = Experience(**{
    **EXPERIENCES_DATABASE['billy_edu'],
    'start_month': Month('September'),
    'end_month': Month('May'),
    'type': ExpType('Education'),
})

billy_edu1 = Achievement(**ACHIEVEMENTS_DATABASE['billy_edu1'])

billy_edu.achievements.append(billy_edu1)
billy.achievements.append(billy_edu1)


# creates billy's work experience
billy_work = Experience(**{
    **EXPERIENCES_DATABASE['billy_work'],
    'start_month': Month('January'),
    'end_month': Month('none'),
    'type': ExpType('Work'),
})
billy_work1 = Achievement(**ACHIEVEMENTS_DATABASE['billy_work1'])
billy_work2 = Achievement(**ACHIEVEMENTS_DATABASE['billy_work2'])
billy_work3 = Achievement(**ACHIEVEMENTS_DATABASE['billy_work3'])

billy_work.achievements.extend([billy_work1, billy_work2, billy_work3])
billy.achievements.extend([billy_work1, billy_work2, billy_work3])


skills = [Skill(id=get_skill_id(name),name=name,)
          for name in SKILLS_NAMES]

advocacy_capability = Capability(
    id='cap:advocacy',
    name='Advocacy and Public Policy',
)
advocacy_recommendations = [
    SkillRecommendation(
        capability_id='cap:advocacy',
        skill_id=get_skill_id(name),
        order=i
    )
    for (i, name) in enumerate([
        'Community Organizing',
        'Canvassing',
        'Advocacy',
        'Policy Writing',
        'Volunteer Mobilization',
    ])
]
outreach_capability = Capability(
    id='cap:outreach',
    name='Community Engagement and Outreach',
)
outreach_recommendations = [
    SkillRecommendation(
        capability_id='cap:outreach',
        skill_id=get_skill_id(name),
        order=i
    )
    for (i, name) in enumerate([
        'Community Engagement',
        'Client Recruitment',
        'Partnership Building',
        'Event Planning',
        'Community Organizing',
    ])
]
it_capability = Capability(
    id='cap:it',
    name='Information Technology',
)

billy_flask_suggestion = CapabilitySkillSuggestion(
    contact_id=123,
    capability_id='cap:it',
    skill_id='QUEVjv1tcq6uLmzCku6ikg=='
)

program_pfp = Program(**{
    **PROGRAMS_DATABASE['pfp'],
    'trello_board_id': '5e37744114d9d01a03ddbcfe'
})

program_mayoral = Program(**{
    **PROGRAMS_DATABASE['mayoral'],
    'trello_board_id': '5e37744114d9d01a03ddbcfe'
})


billy_pfp = ProgramContact(
    id=5,
    program_id=1,
    contact_id=123,
    stage=1,
    is_approved=True
)

billy_mayoral = ProgramContact(
    id=7,
    program_id=2,
    contact_id=123,
    card_id='card',
    stage=1,
    is_approved=False
)

billy_pfp_app = ProgramApp(
    id=7,
    contact_id=123,
    program_id=1,
    is_interested=True,
    is_approved=True,
    decision_date='2020-01-01'
)

billy_mayoral_app = ProgramApp(
    id=8,
    contact_id=123,
    program_id=2,
)

obama_pfp = ProgramContact(
    id=6,
    program_id=1,
    contact_id=124,
    card_id='card',
    stage=1,
)

test_opp1 = Opportunity(
    id='123abc',
    title="Test Opportunity",
    short_description="This is a test opportunity.",
    gdoc_id="ABC123xx==",
    card_id="card",
    gdoc_link="https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit",
    org_name="Test Org",
    program_id=1,
    program_name="Place for Purpose"
)

test_opp2 = Opportunity(
    id='222abc',
    title="Another Test Opportunity",
    short_description="This is another test opportunity.",
    gdoc_id="BBB222xx==",
    card_id="card",
    gdoc_link="https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit",
    org_name="Test Org",
    program_id=2,
    program_name="Mayoral Fellowship"
)

test_opp3 = Opportunity(
    id='333abc',
    title="A Third Test Opportunity",
    short_description="This is another test opportunity.",
    gdoc_id="CCC333xx==",
    card_id="card",
    gdoc_link="https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit",
    org_name="Test Org",
    program_id=1,
    program_name="Place for Purpose"
)

snapshot1 = ResumeSnapshot(
    id=1111,
    resume='{"test":"snapshot1"}',
)

app_billy = OpportunityApp(
    id='a1',
    contact_id=123,
    opportunity_id='123abc',
    interest_statement="I'm interested in this test opportunity",
    stage=1,
    resume_id=1111,
)

app_billy2 = OpportunityApp(
    id='a2',
    contact_id=123,
    opportunity_id='222abc',
    interest_statement="I'm also interested in this test opportunity",
    stage=0,
)

app_obama = OpportunityApp(
    id='a3',
    contact_id=124,
    opportunity_id='123abc',
    interest_statement="I'm also interested in this test opportunity",
    stage=2,
)


def get_skill(name):
    return Skill.query.get(get_skill_id(name))


def populate(db):
    for skill in skills:
        db.session.add(skill)
    db.session.commit()

    db.session.add(billy)
    db.session.add(obama)
    db.session.add(billy_session)
    db.session.add(program_pfp)
    db.session.add(program_mayoral)
    db.session.add(billy_pfp)
    db.session.add(billy_mayoral)
    db.session.add(billy_pfp_app)
    db.session.add(billy_mayoral_app)
    db.session.add(obama_pfp)
    db.session.add(test_opp1)
    db.session.add(test_opp2)
    db.session.add(test_opp3)
    db.session.add(snapshot1)
    db.session.add(app_billy)
    db.session.add(app_billy2)
    db.session.add(app_obama)

    db.session.commit()

    billy.add_skill(get_skill('Public Health'))
    billy.add_skill(get_skill('Community Organizing'))
    obama.add_skill(get_skill('Public Health'))

    billy_work.add_skill(get_skill('Python'))
    billy_work.add_skill(get_skill('Web Development'))
    billy_work1.add_skill(get_skill('Flask'), it_capability)
    billy_work2.add_skill(
        get_skill('Community Organizing'), advocacy_capability)
    billy_work3.add_skill(get_skill('Web Development'), it_capability)
    billy_edu1.add_skill(get_skill('Python'), it_capability)

    billy.add_skill(get_skill('Flask'))
    db.session.add(billy_flask_suggestion)

    # Test deleted skills as well
    billy.add_skill(get_skill('Event Planning'))
    outreach_capability.related_skills.append(get_skill('Event Planning'))
    billy_work2.add_skill(get_skill('Event Planning'))
    billy_eventplan = get_contact_skill(123, 'Event Planning')
    billy_eventplan.deleted = True

    advocacy_capability.related_skills.append(
        get_skill('Community Organizing'))
    outreach_capability.related_skills.append(
        get_skill('Community Organizing'))
    it_capability.related_skills.append(get_skill('Python'))
    it_capability.related_skills.append(get_skill('C++'))
    it_capability.related_skills.append(get_skill('Web Development'))

    db.session.add(advocacy_capability)
    for rec in advocacy_recommendations:
        db.session.add(rec)
    db.session.add(outreach_capability)
    for rec in outreach_recommendations:
        db.session.add(rec)
    db.session.add(it_capability)

    db.session.commit()

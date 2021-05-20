import datetime as dt

# imports models related to the contact
from app.models.contact_model import Contact
from app.models.email_model import Email, Type as EmailType

# imports models related to experiences
from app.models.experience_model import (
    Experience,
    Degree,
    Type as ExpType,
    Month,
)
from app.models.achievement_model import Achievement

# imports models related to skills
from app.models.skill_model import (
    Skill,
    Capability,
    SkillRecommendation,
    CapabilitySkillSuggestion
)
from app.models.skill_item_model import ContactSkill
from app.resources.skill_utils import (
    get_skill_id,
    get_contact_skill,
    make_skill,
)

# imports models related to the resume
from app.models.resume_model import ResumeSnapshot

# imports models related to the program and cycle
from app.models.program_model import Program
from app.models.program_app_model import ProgramApp
from app.models.opportunity_model import Opportunity
from app.models.opportunity_app_model import OpportunityApp
from app.models.session_model import UserSession
from app.models.profile_model import (
    Profile,
    Race,
    ContactAddress,
    RoleChoice,
    ProgramsCompleted
)

from tests.contact.contact_data import CONTACTS_DATABASE, EMAILS_DATABASE
from tests.opportunity.opportunity_data import (
    OPPS_DATABASE,
    OPP_APPS_DATABASE,
    RESUME_SNAPSHOTS
)
from tests.program.program_data import (
    PROGRAMS_DATABASE,
    PROGRAM_APPS_DATABASE
)
from tests.skill.skill_data import SKILLS_NAMES
from tests.experience.experience_data import (
    EXPERIENCES_DATABASE,
    ACHIEVEMENTS_DATABASE
)
from tests.profile.profile_data import (
    ADDRESSES,
    PROGRAMS_COMPLETED,
    RACE,
    ROLES,
    PROFILES_DATABASE
)

# creates billy's contact
billy = Contact(**{**CONTACTS_DATABASE['billy'], 'stage': 3})
billy.email_primary = Email(**EMAILS_DATABASE['billy'])
billy.email_primary.type = EmailType('Personal')


# creates obama's contact
obama = Contact(**CONTACTS_DATABASE['obama'])
obama.email_primary = Email(**EMAILS_DATABASE['obama'])
obama.email_primary.type = EmailType('Work')


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


def create_exp(contact, exp_data):
    exp_data['start_month'] = Month(exp_data['start_month'])
    exp_data['end_month'] = Month(exp_data['end_month'])
    exp_data['type'] = ExpType(exp_data['type'])

    exp = Experience(**exp_data)
    contact.experiences.append(exp)

    return exp

# creates obama's portfolio experience
obama_portfolio = create_exp(obama, EXPERIENCES_DATABASE['obama_portfolio'])


# creates billy's educational experience
billy_edu = create_exp(billy, EXPERIENCES_DATABASE['billy_edu'])
billy_edu1 = Achievement(**ACHIEVEMENTS_DATABASE['billy_edu1'])

billy_edu.achievements.append(billy_edu1)
billy.achievements.append(billy_edu1)


# creates billy's work experience
billy_work = create_exp(billy, EXPERIENCES_DATABASE['billy_work'])
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


# creates program records
program_pfp = Program(**PROGRAMS_DATABASE['pfp'])
program_pfp.trello_board_id = '5e37744114d9d01a03ddbcfe'

program_mayoral = Program(**PROGRAMS_DATABASE['mayoral'])


# creates billy's program apps
billy_pfp_app = ProgramApp(**PROGRAM_APPS_DATABASE['billy_pfp'])
billy_pfp_app.contact = billy
billy_pfp_app.program = program_pfp

billy_mayoral_app = ProgramApp(**PROGRAM_APPS_DATABASE['billy_mayoral'])
billy_mayoral_app.contact = billy
billy_mayoral_app.program = program_mayoral


# creates opportunities
test_opp1 = Opportunity(**OPPS_DATABASE['opp1'])
test_opp2 = Opportunity(**OPPS_DATABASE['opp2'])
test_opp3 = Opportunity(**OPPS_DATABASE['opp3'])


# creates billy's app for test_opp1
app_billy = OpportunityApp(**{**OPP_APPS_DATABASE['billy1'], 'stage': 1})
app_billy.resume = ResumeSnapshot(**RESUME_SNAPSHOTS['snapshot1'])
app_billy.contact = billy
app_billy.opportunity = test_opp1


# creates billy's app for test_opp2
app_billy2 = OpportunityApp(**OPP_APPS_DATABASE['billy2'])
app_billy2.contact = billy
app_billy2.opportunity =  test_opp2


# creates obama's app for test_opp1
app_obama = OpportunityApp(**{**OPP_APPS_DATABASE['obama1'],'stage': 2})
app_obama.contact = obama
app_obama.opportunity = test_opp1


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
    db.session.add(test_opp1)
    db.session.add(test_opp2)
    db.session.add(test_opp3)

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

from datetime import date
# imports models related to the contact
from models.contact_model import (
    Contact,
    Gender,
    Race,
    Salutation,
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

#imports models related to skills
from models.tag_model import (
    Tag,
    TagType,
    TagStatusType,
)
from models.tag_item_model import TagItem
from models.skill_model import Skill, Capability, SkillRecommendation
from models.skill_item_model import ContactSkill
from resources.skill_utils import get_skill_id, make_skill

#imports models related to the resume
#from models.resume_model import Resume
#from models.resume_section_model import ResumeSection
#from models.resume_item_model import ResumeItem

# imports models related to the program and cycle
from models.program_model import Program
from models.program_contact_model import ProgramContact
from models.cycle_model import Cycle
from models.question_model import Question
from models.response_model import Response
from models.review_model import Review

billy = Contact(
    id=123,
    first_name='Billy',
    last_name='Daly',
    email_primary=Email(
        id=45,
        is_primary=True,
        email='billy@example.com',
        type=EmailType.personal,
    ),
    gender='Male',
    birthdate=date(1991, 1, 2),
    phone_primary='555-245-2351',
    race_all='White',
    pronouns='He/Him/His',
    account_id='test-valid|0123456789abcdefabcdefff',
    terms_agreement=True
)
obama = Contact(
    id=124,
    first_name='Barack',
    last_name='Obama',
    email_primary=Email(
        id=90,
        is_primary=True,
        email='obama@whitehouse.gov',
        type=EmailType('Work'),
    ),
    gender='Male',
    birthdate=date(1961, 8, 4),
    phone_primary='555-444-4444',
    race_all='Black or African-American;White',
    race_other='Test',
    pronouns='Not Listed',
    pronouns_other='They/Them/Their',
    terms_agreement=True

)

exp_columbia = Experience(
    id=511,
    host='Columbia University',
    title='Political Science',
    description='Test description',
    link='www.google.com',
    start_month=Month('September'),
    start_year=1979,
    end_month=Month('May'),
    end_year=1983,
    type=ExpType('Accomplishment'),
    location='New York, NY, USA',
    contact_id=124,
)


exp_goucher = Experience(
    id=512,
    host='Goucher College',
    title='Economics',
    degree='Undergraduate',
    degree_other='Study Abroad',
    start_month=Month('September'),
    start_year=2012,
    end_month=Month('May'),
    end_year=2016,
    type=ExpType('Education'),
    location='Towson, MD, USA',
    contact_id=123,
)

exp_baltimore = Experience(
    id=513,
    host='Baltimore Corps',
    description='Test description here',
    title='Systems Design Manager',
    start_month=Month('January'),
    start_year=2000,
    end_month='none',
    end_year=0,
    type=ExpType('Work'),
    location='Baltimore, MD, USA',
    contact_id=123,
)

a_baltimore1 = Achievement(
    id=81,
    exp_id=513,
    contact_id=123,
    description='Redesigned the Salesforce architecture to facilitate easier reporting.'
)
a_baltimore2 = Achievement(
    id=82,
    exp_id=513,
    contact_id=123,
    description='Formalized organizational strategy for defining and analyzing KPIs.'
)
a_baltimore3 = Achievement(
    id=83,
    exp_id=513,
    contact_id=123,
    description='Developed recruitment projection tools to model and track progress to goals.'
)
a_goucher1 = Achievement(
    id=84,
    exp_id=512,
    contact_id=123,
    description='Did some stuff'
)


#tag_python = Tag(
#    id=123,
#    name='Python',
#    type=TagType('Skill'),
#    status=TagStatusType('Active'),
#)
#
#tag_webdev = Tag(
#    id=124,
#    name='Web Development',
#    type=TagType('Function'),
#    status=TagStatusType('Active'),
#)
#tag_health = Tag(
#    id=125,
#    name='Public Health',
#    type=TagType('Topic'),
#    status=TagStatusType('Active'),
#)
#
#item_webdev = TagItem(
#    id=21,
#    contact_id=123,
#    tag_id=124,
#    score=2
#)
#
#resume_billy = Resume(
#    id=51,
#    contact_id=123,
#    name="Billy's Resume",
#    date_created=date(2019,5,4),
#    gdoc_id="abcdefghijklmnopqrstuvwxyz1234567890-_",
#)

skills = [
    Skill(
        id=get_skill_id(name),
        name=name,
    ) 
    for name in [
        'Python',
        'C++',
        'Web Development',
        'Public Health',
        'Advocacy and Public Policy',
        'Community Organizing',
        'Canvassing',
        'Advocacy',
        'Policy Writing',
        'Volunteer Mobilization',
        'Community Engagement and Outreach',
        'Community Engagement',
        'Client Recruitment',
        'Partnership Building',
        'Event Planning',
        'Information Technology',
    ]
]

advocacy_capability = Capability(
    id='cap:advocacy',
    name='Advocacy and Public Policy',
    cap_skill_id=get_skill_id('Advocacy and Public Policy')
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
advocacy_capability = Capability(
    id='cap:advocacy',
    name='Advocacy and Public Policy',
    cap_skill_id=get_skill_id('Advocacy and Public Policy')
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
    cap_skill_id=get_skill_id('Community Engagement and Outreach')
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
    cap_skill_id=get_skill_id('Information Technology')
)


#skill_python = SkillItem(
#    id=get_skill_id('Python'),
#    name='Python',
#    contact_id=123,
#)
#skill_webdev = SkillItem(
#    id=get_skill_id('Web Development'),
#    name='Web Development',
#    contact_id=123,
#)
#skill_health = SkillItem(
#    id=get_skill_id('Public Health'),
#    name='Public Health',
#    contact_id=123,
#)
#
#skill_obama_health = SkillItem(
#    id=get_skill_id('Public Health'),
#    name='Public Health',
#    contact_id=124,
#)



program_pfp = Program(
    id=1,
    name='Place for Purpose',
)

cycle_pfp = Cycle(
    id=2,
    program_id=1,
    date_start=date(2020, 1, 6),
    date_end=date(2025, 1, 6),
    intake_talent_board_id='5e37744114d9d01a03ddbcfe',
    intake_org_board_id='intake_org',
    match_talent_board_id='match_talent',
    match_opp_board_id='match_opp',
    review_talent_board_id='5e3753cdaea77d37fce3496a',
)

q_pfp1 = Question(
    id=3,
    program_id=1,
    question_text='Race and equity',
    limit_word=200,
    limit_character=2000,
)

q_pfp2 = Question(
    id=4,
    program_id=1,
    question_text='Sector effectiveness',
    limit_word=300,
    limit_character=3000,
)

billy_pfp = ProgramContact(
    id=5,
    program_id=1,
    contact_id=123,
    card_id='card',
    stage=1,
)

r_billy1 = Response(
    id=6,
    program_contact_id=5,
    question_id=3,
    response_text='Race and equity answer',
)

r_billy2 = Response(
    id=7,
    program_contact_id=5,
    question_id=4,
    response_text='Sector effectiveness answer',
)

review_billy = Review(
    id=1,
    program_contact_id=5,
    card_id='card_id',
    score=1,
    stage=1,
)

def get_skill(name):
    return Skill.query.get(get_skill_id(name))


def populate(db):
    for skill in skills:
        db.session.add(skill)
    db.session.commit()

    db.session.add(billy)
    db.session.add(obama)
    db.session.add(exp_columbia)
    db.session.add(exp_goucher)
    db.session.add(exp_baltimore)
    db.session.add(a_goucher1)
    db.session.add(a_baltimore1)
    db.session.add(a_baltimore2)
    db.session.add(a_baltimore3)
    #db.session.add(tag_python)
    #db.session.add(tag_webdev)
    #db.session.add(tag_health)
    #db.session.add(item_webdev)
    #db.session.add(resume_billy)
    #db.session.add(skill_python)
    #db.session.add(skill_webdev)
    #db.session.add(skill_health)
    #db.session.add(skill_obama_health)
    db.session.add(program_pfp)
    db.session.add(cycle_pfp)
    db.session.add(q_pfp1)
    db.session.add(q_pfp2)
    db.session.add(billy_pfp)
    db.session.add(r_billy1)
    db.session.add(r_billy2)
    db.session.add(review_billy)

    db.session.commit()

    billy.add_skill(get_skill('Public Health'))
    billy.add_skill(get_skill('Community Organizing'))
    obama.add_skill(get_skill('Public Health'))
    exp_baltimore.add_skill(get_skill('Python'))
    exp_baltimore.add_skill(get_skill('Web Development'))

    advocacy_capability.related_skills.append(get_skill('Community Organizing'))
    outreach_capability.related_skills.append(get_skill('Community Organizing'))
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

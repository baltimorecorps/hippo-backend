from datetime import date
from resources.skill_utils import get_skill_id

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
from models.experience_model import (
    Experience,
    Degree,
    Type as ExpType,
    Month,
)

from models.achievement_model import (
    Achievement
)

from models.tag_model import (
    Tag,
    TagType,
    TagStatusType,
)

from models.tag_item_model import (
    TagItem,
)

from models.skill_model import (
    SkillItem,
)

from models.resume_model import (
    Resume,
)
from models.resume_section_model import (
    ResumeSection,
)
from models.resume_item_model import (
    ResumeItem,
)

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
    gender=Gender('Male'),
    birthdate=date(1991, 1, 2),
    phone_primary='555-245-2351',
    race_all=Race('White'),
    account_id='billy|123'
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
    gender=Gender('Male'),
    birthdate=date(1961, 8, 4),
    phone_primary='555-444-4444',
    race_all=Race('Black'),
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


tag_python = Tag(
    id=123,
    name='Python',
    type=TagType('Skill'),
    status=TagStatusType('Active'),
)

tag_webdev = Tag(
    id=124,
    name='Web Development',
    type=TagType('Function'),
    status=TagStatusType('Active'),
)
tag_health = Tag(
    id=125,
    name='Public Health',
    type=TagType('Topic'),
    status=TagStatusType('Active'),
)

item_webdev = TagItem(
    id=21,
    contact_id=123,
    tag_id=124,
    score=2
)

resume_billy = Resume(
    id=51,
    contact_id=123,
    name="Billy's Resume",
    date_created=date(2019,5,4),
    gdoc_id="abcdefghijklmnopqrstuvwxyz1234567890-_",
)

skill_python = SkillItem(
    id=get_skill_id('Python'),
    name='Python',
    contact_id=123,
)
skill_webdev = SkillItem(
    id=get_skill_id('Web Development'),
    name='Web Development',
    contact_id=123,
)
skill_health = SkillItem(
    id=get_skill_id('Public Health'),
    name='Public Health',
    contact_id=123,
)

skill_obama_health = SkillItem(
    id=get_skill_id('Public Health'),
    name='Public Health',
    contact_id=124,
)



def populate(db):
    exp_baltimore.skills.append(skill_python)
    exp_baltimore.skills.append(skill_webdev)
    db.session.add(billy)
    db.session.add(obama)
    db.session.add(exp_columbia)
    db.session.add(exp_goucher)
    db.session.add(exp_baltimore)
    db.session.add(a_goucher1)
    db.session.add(a_baltimore1)
    db.session.add(a_baltimore2)
    db.session.add(a_baltimore3)
    db.session.add(tag_python)
    db.session.add(tag_webdev)
    db.session.add(tag_health)
    db.session.add(item_webdev)
    db.session.add(resume_billy)
    db.session.add(skill_python)
    db.session.add(skill_webdev)
    db.session.add(skill_health)
    db.session.add(skill_obama_health)
    db.session.commit()

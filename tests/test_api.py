import json
import datetime as dt
from pprint import pprint
import pytest
import math


from models.contact_model import Contact
from models.experience_model import Experience, Month
from models.resume_model import Resume
from models.resume_section_model import ResumeSection
from models.program_contact_model import ProgramContact
from models.session_model import UserSession
from models.opportunity_model import Opportunity
from models.opportunity_app_model import OpportunityApp, ApplicationStage

from models.skill_model import (
    CapabilitySkillSuggestion
)
from models.skill_item_model import (
    ContactSkill,
    ExperienceSkill,
    AchievementSkill,
)

from flask import g

SKILLS = {
    'billy': [
        {
            'id': '74BgThI2os9wEdyArofEKA==',
            'name': 'Community Organizing',
        },
        {
            'id': 'QUEVjv1tcq6uLmzCku6ikg==',
            'name': 'Flask',
        },
        {
            'id': 'n1N02ypni69EZg0SggRIIg==',
            'name': 'Public Health',
        },
        {
            'id': '4R9tqGuK2672PavRTJrN_A==',
            'name': 'Python',
        },
        {
            'id': 'hbBWJS6x6gDxGMUC5HAOYg==',
            'name': 'Web Development',
        },
    ],
    'obama': [
        {
            'id': 'n1N02ypni69EZg0SggRIIg==',
            'name': 'Public Health',
        },
    ],
}

CAPABILITIES = {
    'billy': {
        'contact_id': 123,
        'capabilities': [
            {
                'id': 'cap:it',
                'name': 'Information Technology',
                'score': 2,
                'skills': [
                    {'id': '4R9tqGuK2672PavRTJrN_A==', 'name': 'Python'},
                    {'id': 'hbBWJS6x6gDxGMUC5HAOYg==', 'name': 'Web Development'}
                ],
                'suggested_skills': [
                    {'id': 'QUEVjv1tcq6uLmzCku6ikg==', 'name': 'Flask'}
                ]
            },
            {
                'id': 'cap:advocacy',
                'name': 'Advocacy and Public Policy',
                'score': 1,
                'skills': [
                    {'id': '74BgThI2os9wEdyArofEKA==', 'name': 'Community Organizing'}
                ],
                'suggested_skills': []
            },
            {
                'id': 'cap:outreach',
                'name': 'Community Engagement and Outreach',
                'score': 0,
                'skills': [
                    {'id': '74BgThI2os9wEdyArofEKA==', 'name': 'Community Organizing'}
                ],
                'suggested_skills': []
            }
        ],
        'other_skills': [
            { 'id': 'n1N02ypni69EZg0SggRIIg==', 'name': 'Public Health'}
        ]
    }
}



QUESTIONS = {
    'q_pfp1': {
        'id': 3,
        'program_id': 1,
        'question_text': 'Race and equity',
        'limit_word': 200,
        'limit_character': 2000
    },
    'q_pfp2': {
        'id': 4,
        'program_id': 1,
        'question_text': 'Sector effectiveness',
        'limit_word': 300,
        'limit_character': 3000
    }
}

CYCLES = {
    'pfp': {
        'id': 2,
        'program_id': 1,
        'date_start': '2020-01-06',
        'date_end': '2025-01-06',
        'intake_talent_board_id': '5e37744114d9d01a03ddbcfe',
        'intake_org_board_id': 'intake_org',
        'match_talent_board_id': 'match_talent',
        'match_opp_board_id': '5e4acd35a35ee523c71f9e25',
        'is_active': True,
        'review_talent_board_id': '5e3753cdaea77d37fce3496a'
    }
}

PROGRAMS = {
    'pfp': {
        'id': 1,
        'name': 'Place for Purpose',
        'current_cycle': CYCLES['pfp']
    }
}

RESPONSES = {
    'r_billy1': {
        'id': 6,
        'program_contact_id': 5,
        'question_id': 3,
        'response_text': 'Race and equity answer'
    },
    'r_billy2': {
        'id': 7,
        'program_contact_id': 5,
        'question_id': 4,
        'response_text': 'Sector effectiveness answer'
    }
}

REVIEWS = {
    'review_billy': {
        'id': 1,
        'score': 1,
        'stage': 1,
        'is_active': True,
        'card_id': 'card_id'
    }
}

PROGRAM_CONTACTS = {
    'billy_pfp': {
        'id': 5,
        'contact_id': 123,
        'program': PROGRAMS['pfp'],
        'card_id': 'card',
        'stage': 1,
        'is_active': True,
        'is_approved': True,
        'reviews': [
            REVIEWS['review_billy']
        ]
    }
}

ELIGIBILITY = {
    'billy_pfp': {
        'id': 5,
        'contact_id': 123,
        'program_id': 1,
        'cycles': [2],
        'stage': 1,
        'is_active': True,
        'is_approved': True,
    }
}

OPPORTUNITIES = {
    'test_opp1': {
        'id': '123abc',
        'title': "Test Opportunity",
        'short_description': "This is a test opportunity.",
        'gdoc_id': "ABC123xx==",
        'gdoc_link': "https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit",
        'status': 'submitted',
        'org_name': 'Test Org',
        'cycle_id': 2,
        'program_id': 1
    },
    'test_opp2': {
        'id': '222abc',
        'title': "Another Test Opportunity",
        'short_description': "This is another test opportunity.",
        'gdoc_id': "BBB222xx==",
        'gdoc_link': "https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit",
        'status': 'submitted',
        'org_name': 'Test Org',
        'cycle_id': 2,
        'program_id': 1
    },

}


CONTACTS = {
    'billy': {
        'id': 123,
        'first_name': "Billy",
        'last_name': "Daly",
        'email_primary': {
            'id': 45,
            'is_primary': True,
            'email': "billy@example.com",
            'type': "Personal",
        },
        'emails': [{
            'id': 45,
            'is_primary': True,
            'email': "billy@example.com",
            'type': "Personal",
        }],
        'gender': 'Male',
        'gender_other': None,
        'birthdate': '1991-01-02',
        'phone_primary': "555-245-2351",
        'race_all': "White",
        'race_other': None,
        'pronouns': 'He/Him/His',
        'pronouns_other': None,
        'account_id': 'test-valid|0123456789abcdefabcdefff',
        'skills': SKILLS['billy'],
        'programs': [PROGRAM_CONTACTS['billy_pfp']],
        'terms_agreement': True
    },

    'obama': {
        'id': 124,
        'first_name': "Barack",
        'last_name': "Obama",
        'email_primary': {
            'id': 90,
            'is_primary': True,
            'email': "obama@whitehouse.gov",
            'type': "Work",
        },
        'emails': [{
            'id': 90,
            'is_primary': True,
            'email': "obama@whitehouse.gov",
            'type': "Work",
        }],
        'gender': 'Male',
        'gender_other': None,
        'birthdate': '1961-08-04',
        'phone_primary': "555-444-4444",
        'race_all': "Black or African-American;White",
        'race_other': 'Test',
        'pronouns': 'Not Listed',
        'pronouns_other': 'They/Them/Their',
        'account_id': None,
        'skills': SKILLS['obama'],
        'programs': [],
        'terms_agreement': True
    },
}

SNAPSHOTS = {
    'snapshot1': {
        'test': 'snapshot1'
    },
    'snapshot2': {
        'test': 'snapshot2'
    },
}

APPLICATIONS = {
    'app_billy': {
        'id': 'a1',
        'contact': CONTACTS['billy'],
        'opportunity': OPPORTUNITIES['test_opp1'],
        'interest_statement': "I'm interested in this test opportunity",
        'status': 'submitted',
        'resume': SNAPSHOTS['snapshot1'],
    },
    'app_billy2': {
        'id': 'a2',
        'contact': CONTACTS['billy'],
        'opportunity': OPPORTUNITIES['test_opp2'],
        'interest_statement': "I'm also interested in this test opportunity",
        'status': 'draft',
    },

}


ACHIEVEMENTS = {
    'baltimore1': {
        'id': 81,
        'description': 'Redesigned the Salesforce architecture to facilitate easier reporting.',
        'skills': [{
            'name': 'Flask', 'capability_id': 'cap:it',
        }],
    },
    'baltimore2': {
        'id': 82,
        'description': 'Formalized organizational strategy for defining and analyzing KPIs.',
        'skills': [{
            'name': 'Community Organizing', 'capability_id': 'cap:advocacy',
        }],
    },
    'baltimore3': {
        'id': 83,
        'description': 'Developed recruitment projection tools to model and track progress to goals.',
        'skills': [{
            'name': 'Web Development', 'capability_id': 'cap:it',
        }],
    },
    'goucher1': {
        'id': 84,
        'description': 'Did some stuff',
        'skills': [{
            'name': 'Python', 'capability_id': 'cap:it',
        }],
    }
}

DATE_START = dt.date(2000, 1, 1)
DATE_END = dt.datetime.today()
DATE_LENGTH = ((DATE_END.year - DATE_START.year) * 12
               + DATE_END.month - DATE_START.month)

#Changes made to the EXPERIENCES constant also need to be
#made to the data in the populate_db.py script
#in the common directory

EXPERIENCES = {
    'columbia': {
        'id': 511,
        'description': 'Test description',
        'host': 'Columbia University',
        'title': 'Political Science',
        'degree': None,
        'degree_other': None,
        'link': 'www.google.com',
        'is_current': False,
        'start_month': 'September',
        'start_year': 1979,
        'end_month': 'May',
        'end_year': 1983,
        'length_year': 3,
        'length_month': 8,
        'type': 'Accomplishment',
        'contact_id': 124,
        'location': 'New York, NY, USA',
        'achievements': [],
        'skills': [
        ],
    },
    'goucher': {
        'id': 512,
        'description': None,
        'host': 'Goucher College',
        'title': 'Economics',
        'degree': 'Undergraduate',
        'degree_other': 'Study Abroad',
        'link': None,
        'is_current': False,
        'start_month': 'September',
        'start_year': 2012,
        'end_month': 'May',
        'end_year': 2016,
        'length_year': 3,
        'length_month': 8,
        'type': 'Education',
        'contact_id': 123,
        'location': 'Towson, MD, USA',
        'achievements': [
            ACHIEVEMENTS['goucher1'],
        ],
        'skills': [
            SKILLS['billy'][3],
        ],
    },
    'baltimore' : {
        'id': 513,
        'description': 'Test description here',
        'host': 'Baltimore Corps',
        'title': 'Systems Design Manager',
        'degree': None,
        'degree_other': None,
        'link': None,
        'is_current': True,
        'start_month': 'January',
        'start_year': 2000,
        'end_month': 'none',
        'end_year': 0,
        'length_year': math.floor(DATE_LENGTH/12),
        'length_month': DATE_LENGTH % 12,
        'type': 'Work',
        'contact_id': 123,
        'location': 'Baltimore, MD, USA',
        'achievements': [
            ACHIEVEMENTS['baltimore1'],
            ACHIEVEMENTS['baltimore2'],
            ACHIEVEMENTS['baltimore3'],
        ],
        'skills': SKILLS['billy'][0:2] + SKILLS['billy'][3:5],
    },
}

TAGS = {
    'python': {
        'id': 123,
        'name': 'Python',
        'type': 'Skill',
        'status': 'Active',
    },
    'webdev': {
        'id': 124,
        'name': 'Web Development',
        'type': 'Function',
        'status': 'Active',
    },
    'health': {
        'id': 125,
        'name': 'Public Health',
        'type': 'Topic',
        'status': 'Active',
    },
}

TAG_ITEMS = {
    'billy_webdev': {
        'id': 21,
        'name': 'Web Development',
        'type': 'Function',
        'contact_id': 123,
        'tag_id': 124,
        'score': 2,
    }
}

# This is kind of gross -- maybe we should consider standardizing the resume
# responses so that they're the same as everything else?
def filter_dict(d, keys):
    return {k:v for k, v in d.items() if k not in keys}

RESUME_SECTIONS = {
    'billy_work': {
        'id': 61,
        'resume_id': 51,
        'max_count': None,
        'min_count': None,
        'name': "Work Experience",
        'items': [
            {
                'resume_order': 0,
                'indented': False,
                'achievement': None,
                'tag': None,
                'experience': filter_dict(EXPERIENCES['baltimore'],
                                          {'achievements', 'contact_id'}),
            },
        ],
    },
    'billy_skills': {
        'id': 62,
        'resume_id': 51,
        'max_count': None,
        'min_count': None,
        'name': "Skills",
        'items': [
            {
                'resume_order': 0,
                'indented': False,
                'achievement': None,
                'experience': None,
                'tag': filter_dict(TAG_ITEMS['billy_webdev'], {'contact_id'}),
            },
        ],
    },
}

RESUMES = {
    'billy': {
        'id': 51,
        'contact': CONTACTS['billy'],
        'name': "Billy's Resume",
        'date_created': '2019-05-04',
        'gdoc_id': 'abcdefghijklmnopqrstuvwxyz1234567890-_',
    },
}

RESUME_OUTPUT = {
    'name': 'Billy Resume',
    'date_created': dt.datetime.today().strftime('%Y-%m-%d'),
    'contact': CONTACTS['billy'],
    'gdoc_link': None,
    'relevant_exp_dump': [EXPERIENCES['goucher']],
    'other_exp_dump': [EXPERIENCES['baltimore']],
    'relevant_edu_dump': [EXPERIENCES['goucher']],
    'other_edu_dump': [EXPERIENCES['baltimore']],
    'relevant_achieve_dump': [EXPERIENCES['baltimore']],
    'other_achieve_dump': [EXPERIENCES['goucher']],
    'relevant_skills_dump': [TAG_ITEMS['billy_webdev']],
    'other_skills_dump': [TAG_ITEMS['billy_webdev']]
}

POSTS = {
    'experience': {
        'description': 'Test description',
        'host': 'Test Org',
        'title': 'Test title',
        'start_month': 'September',
        'start_year': 2000,
        'end_month': 'May',
        'end_year': 2019,
        'type': 'Work',
        'contact_id': 123,
        'location': 'Test City, MD, USA',
        'achievements': [
            {'description': 'Test achievement 1'},
            {'description': 'Test achievement 2', 'skills': [
                { 'name': 'Community Organizing', 'capability_id': 'cap:advocacy' },
                { 'name': 'Test Skill 1' }
            ]},
        ],
    },
    'resume': {
        'name': 'Billy Resume',
        'gdoc_link': None,
        'contact_id': 123,
        'relevant_exp': [512],
        'other_exp': [513],
        'relevant_edu': [512],
        'other_edu': [513],
        'relevant_achieve': [513],
        'other_achieve': [512],
        'relevant_skills': [21],
        'other_skills': [21],
    },
    'program_contact': {
        'id': 5,
        'program_id': 1,
        'contact_id': 124,
        'card_id': 'card',
        'stage': 1
    },
    'contact': {
        "first_name": "Tester",
        "last_name": "Byte",
        "email_primary": {
            "email": "testerb@example.com",
            "is_primary": True,
        },
        "phone_primary": "111-111-1111",
        "gender": "Female",
        "race_all": "Hispanic/Latino;Other",
        "race_other": "Cuban",
        "pronouns": "She/Her/Hers",
        "birthdate": "1973-04-23",
        "account_id": 'test-valid|0123456789',
        "terms_agreement": True
    },
    'opportunity': {
        "title": "Test Opportunity",
        "short_description": "We are looking for a tester to test our application by taking this test opportunity. Testers of all experience welcome",
        "gdoc_id": "TESTABC11==",
        "cycle_id": 2,
        "org_name": 'Test Org',
        "gdoc_link": "https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit"
    },
}

def post_request(app, url, data):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    with app.test_client() as client:
        response = client.post(url, data=json.dumps(data),
                               headers=headers)
        pprint(response.json)
        assert response.status_code == 201
        data = json.loads(response.data)['data']
        assert len(data) > 0
        assert data['id'] is not None
        id = data['id']
        return id, data


@pytest.mark.parametrize(
    "url,data,query",
    [pytest.param('/api/contacts/',
      POSTS['contact'],
      lambda id: Contact.query.get(id),
      marks=pytest.mark.skip
      # TODO: unskip when trello stuff is mocked out
      )
    ,('/api/contacts/123/experiences/',
      POSTS['experience'],
      lambda id: Experience.query.get(id)
      )
    ,('/api/contacts/123/skills/',
      {
        'name': 'C++',
      },
      lambda id: ContactSkill.query.filter_by(
          skill_id='sEVDZsMOqdfQ-vwoIAEk5A==', contact_id=123).first()
      )
     ,('/api/contacts/123/capabilities/cap:it/suggestion/',
      {
        'name': 'Network Architecture',
      },
      lambda id: CapabilitySkillSuggestion.query.get(
          (123, 'cap:it', '_s-apdaP_WZpH69G8hlcGA=='))
      )

    ,pytest.param('/api/contacts/124/programs/',
      POSTS['program_contact'],
      lambda id: ProgramContact.query.filter_by(contact_id=124,program_id=1).first(),
      marks=pytest.mark.skip
      # TODO: unskip when trello stuff is mocked out
      )
    ,('/api/opportunity/',
      POSTS['opportunity'],
      lambda id: Opportunity.query.filter_by(title="Test Opportunity").first()
      )
    ,pytest.param('/api/contacts/124/app/123abc/',
      {},
      lambda id: (OpportunityApp.query
                  .filter_by(contact_id=124, opportunity_id='123abc').first()),
      )

    ]
)
def test_post(app, url, data, query):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    id_, _ = post_request(app, url, data)
    assert query(id_) is not None


@pytest.mark.skip
def test_create_program_contact_with_contact(app):
    id_, _ = post_request(app, '/api/contacts/', POSTS['contact'])
    program_contacts = Contact.query.get(id_).programs
    assert len(program_contacts) == 1
    assert program_contacts[0].program_id == 1
    assert program_contacts[0].stage == 1
    assert program_contacts[0].program.name == 'Place for Purpose'
    assert program_contacts[0].is_active == True
    assert program_contacts[0].is_approved == False

def test_post_experience_date(app):
    id_, _ = post_request(app, '/api/contacts/123/experiences/',
                          POSTS['experience'])
    assert Experience.query.get(id_).end_month == Month.may
    assert Experience.query.get(id_).end_year == 2019
    assert Experience.query.get(id_).start_month == Month.september
    assert Experience.query.get(id_).start_year == 2000

def test_post_opportunity_app_status(app):
    id_, _ = post_request(app, '/api/contacts/124/app/123abc/', {})
    assert OpportunityApp.query.get(id_).stage == ApplicationStage.draft.value

def test_post_experience_null_start_date(app):
    exp = POSTS['experience'].copy()
    exp['start_month'] = 'none'
    exp['start_year'] = 0
    id_, _ = post_request(app, '/api/contacts/123/experiences/', exp)
    assert Experience.query.get(id_) is not None
    assert Experience.query.get(id_).start_month == Month.none
    assert Experience.query.get(id_).start_year == 0
    pprint(Experience.query.get(id_).start_month)
    pprint(Experience.query.get(id_).start_year)

def test_post_experience_current(app):
    exp = POSTS['experience'].copy()
    exp['end_month'] = 'none'
    exp['end_year'] = 0
    id_, _ = post_request(app, '/api/contacts/123/experiences/', exp)
    assert Experience.query.get(id_) is not None
    assert Experience.query.get(id_).is_current == True

def test_post_experience_dump_only(app):
    exp = POSTS['experience'].copy()
    exp['length_year'] = 18
    exp['length_month'] = 8
    exp['is_current'] = False
    exp['id'] = 1
    id_, _ = post_request(app, '/api/contacts/123/experiences/', exp)
    assert Experience.query.get(id_) is not None

def test_post_experience_skills(app):
    exp = POSTS['experience'].copy()
    exp['skills'] = [{'name': 'C++'}, {'name': 'Python'}]
    id_, _ = post_request(app, '/api/contacts/123/experiences/', exp)
    assert Experience.query.get(id_).skills[0].name == 'C++'
    assert Experience.query.get(id_).skills[1].name == 'Community Organizing'
    assert Experience.query.get(id_).skills[2].name == 'Python'
    assert Experience.query.get(id_).skills[3].name == 'Test Skill 1'

def test_post_experience_achievement_skills(app):
    exp = POSTS['experience']
    id_, _ = post_request(app, '/api/contacts/123/experiences/', exp)
    skills = Experience.query.get(id_).achievements[1].skills
    assert len(Experience.query.get(id_).achievements[1].skills) == 2
    assert skills[0]['name'] == 'Community Organizing'
    assert skills[0]['capability_id'] == 'cap:advocacy'
    assert skills[1]['name'] == 'Test Skill 1'
    assert skills[1]['capability_id'] is None


def test_post_contact_skill(app):
    url, update = ('/api/contacts/123/skills/', { 'name': 'C++', })

    _, response = post_request(app, url, update)
    assert 'suggested_capabilities' in response
    assert response['suggested_capabilities'] == []
    assert 'capabilities' in response
    assert len(response['capabilities']) == 1
    assert response['capabilities'][0]['id'] == 'cap:it'

    contact_skill = ContactSkill.query.filter_by(
        contact_id=123,
        skill_id='sEVDZsMOqdfQ-vwoIAEk5A==',
        deleted=False,
    ).first()
    assert contact_skill is not None

def test_post_contact_skill_suggestion(app):
    url, update = (
        '/api/contacts/123/capabilities/cap:it/suggestion/',
        {
            'name': 'Network Architecture',
        }
    )

    _, response = post_request(app, url, update)
    assert 'capabilities' in response
    assert response['capabilities'] == []
    assert 'suggested_capabilities' in response
    assert len(response['suggested_capabilities']) == 1
    assert response['suggested_capabilities'][0]['id'] == 'cap:it'

    contact_skill = ContactSkill.query.filter_by(
        contact_id=123,
        skill_id='_s-apdaP_WZpH69G8hlcGA==',
        deleted=False,
    ).first()
    assert contact_skill is not None

def test_post_contact_skill_undelete(app):
    url, update = ('/api/contacts/123/skills/', { 'name': 'Event Planning', })

    _, response = post_request(app, url, update)
    exp = Experience.query.get(513)
    exp_skills = list(map(lambda s: s.name, exp.skills))
    print(exp_skills)
    assert 'Event Planning' in exp_skills
    achievement_skills = list(map(lambda s: s['name'], exp.achievements[1].skills))
    print(achievement_skills)
    assert 'Event Planning' in achievement_skills


# TODO: unskip when trello stuff is mocked out
@pytest.mark.skip
def test_post_contact(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer test-valid|0123456789',
    }
    with app.test_client() as client:
        response = client.post('/api/contacts/',
                               data=json.dumps(POSTS['contact']),
                               headers=headers)
        assert response.status_code == 201
        set_cookie = response.headers.get('set-cookie')
        assert set_cookie is not None
        assert set_cookie.find('HttpOnly;') is not -1
        # Note: Can't test "secure" due to non-https connection
        contact = Contact.query.filter_by(account_id='test-valid|0123456789').first()
        assert contact.first_name == 'Tester'

        assert UserSession.query.filter_by(contact_id=contact.id).first()

def test_post_session(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer test-valid|0123456789abcdefabcdefff',
    }
    with app.test_client() as client:
        response = client.post('/api/session/', headers=headers)
        assert response.status_code == 201
        set_cookie = response.headers.get('set-cookie')
        assert set_cookie is not None
        assert set_cookie.find('HttpOnly;') is not -1
        # Note: Can't test "secure" due to non-https connection

        assert UserSession.query.filter_by(contact_id=123).first().contact.first_name == 'Billy'


@pytest.mark.skip
def test_post_formassembly_opportunity_intake(app):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
    }

    gdoc_id ='1b5erb67lgwvxj-g8u2iitvihhti6_nv-7dehdh8ldfw'

    url = '/api/form-assembly/opportunity-app/'
    data = f'google_doc_id={gdoc_id}&org=Balti&title=QA+Tester&salary_lower=50000&salary_upper=60000&google_doc_link=&capabilities%5B0%5D=tfa_16677&capabilities%5B1%5D=tfa_16678&supervisor_first_name=Billy&supervisor_last_name=Daly&supervisor_title=Director+of+Data&supervisor_email=billy%40baltimorecorps.org&supervisor_phone=4436408904&is_supervisor=tfa_16674&race=tfa_16656&gender=tfa_16662&pronouns=tfa_16668&response_id=157007055'

    with app.test_client() as client:
        response = client.post(url, data=data, headers=headers)
        pprint(response.json)
        assert response.status_code == 201
        data = json.loads(response.data)['data']

        assert 'gdoc_id' in data
        assert data['gdoc_id'] == gdoc_id
        assert 'title' in data
        assert data['title'] == 'QA Tester'

        opp = Opportunity.query.filter_by(gdoc_id=gdoc_id).first()
        assert opp is not None
        assert opp.title == 'QA Tester'

def skill_name(skill):
    return skill.name

@pytest.mark.parametrize(
    "url,update,query,test",
    [('/api/contacts/123/',
      {'first_name': 'William', 'last_name':'Daly',
       'gender': None, 'birthdate': None},
      lambda: Contact.query.get(123),
      lambda e: e.first_name == 'William' and e.gender == None,
      ),
     ('/api/contacts/123/',
      {'first_name': 'William', 'programs': 'This should be excluded from load'},
       lambda: Contact.query.get(123),
       lambda e: e.first_name == 'William'
     ),
     ('/api/contacts/123/',
      {'skills': [
          { 'name': 'Python' },
          { 'name': 'Workforce Development' },
      ]},
      lambda: Contact.query.get(123),
      lambda e: (len(e.skills) == 2
                 and sorted(e.skills, key=skill_name)[0].name == 'Python'
                 and sorted(e.skills, key=skill_name)[1].name == 'Workforce Development'),
      ),
     ('/api/experiences/512/',
      {'end_month': 'January', 'end_year': 2017},
      lambda: Experience.query.get(512),
      lambda e: e.end_month == Month.january and e.end_year == 2017,
      )
    ,('/api/experiences/512/',
      {'achievements': EXPERIENCES['goucher']['achievements'] + [
          {'description': 'test'}
      ]},
      lambda: Experience.query.get(512),
      lambda e: e.achievements[-1].description == 'test',
      )
    ,('/api/experiences/513/',
      {'achievements': EXPERIENCES['baltimore']['achievements'][0:2] + [{
          'id': 83,
          'description': 'Developed recruitment projection tools to model and track progress to goals.',
          'skills': [{'name': 'Python', 'capability_id': 'cap:it'}],
      }]},
      lambda: Experience.query.get(513),
      lambda e: (len(e.achievements[-1].skills) == 1
                 and e.achievements[-1].skills[0]['name'] == 'Python'
                 and e.achievements[-1].skills[0]['capability_id'] == 'cap:it'),
      )
    ,('/api/experiences/513/',
      {'achievements': EXPERIENCES['baltimore']['achievements'][0:2] + [{
          'id': 83,
          'description': 'Developed recruitment projection tools to model and track progress to goals.',
          'skills': [{'name': 'Recruitment', 'capability_id': 'cap:outreach'}],
      }]},
      lambda: Experience.query.get(513),
      lambda e: (len(e.achievements[-1].skills) == 1
                 and e.achievements[-1].skills[0]['name'] == 'Recruitment'
                 and e.achievements[-1].skills[0]['capability_id'] == 'cap:outreach'),
      )

    ,('/api/experiences/513/',
      {'skills': SKILLS['billy'][0:2] + [{'name': 'Test'}]},
      lambda: Experience.query.get(513),
      lambda e: (len(e.skills) == 3
                 and sorted(e.skills, key=skill_name)[0].name == 'Community Organizing'
                 and sorted(e.skills, key=skill_name)[1].name == 'Flask'
                 and sorted(e.skills, key=skill_name)[2].name == 'Test'),
      )
    ,('/api/contacts/123/programs/1/',
      {'stage': 2},
      lambda: ProgramContact.query.get(5),
      lambda r: r.stage == 2,
      )
    ,pytest.param('/api/contacts/123/programs/1/',
      {'responses': [RESPONSES['r_billy1']]},
      lambda: ProgramContact.query.get(5),
      lambda r: len(r.responses) == 1 and r.responses[0].response_text == 'Race and equity answer',
      marks=pytest.mark.skip
      )
    ,pytest.param('/api/opportunity/123abc/',
      {'title': "New title"},
      lambda: Opportunity.query.get('123abc'),
      lambda r: r.title == 'New title',
      marks=pytest.mark.skip
      )
    ,('/api/contacts/123/app/123abc',
      {'interest_statement': "New interest statement", 'resume': None},
      lambda: OpportunityApp.query.get('a1'),
      lambda r: r.interest_statement == 'New interest statement',
      )
    ,('/api/contacts/123/app/123abc',
      {'resume': {'test': 'snapshotnew'}},
      lambda: OpportunityApp.query.get('a1'),
      lambda r: r.resume.resume == '{"test":"snapshotnew"}',
      )
    ,('/api/contacts/123/app/222abc',
      {'resume': {'test': 'snapshotnew'}},
      lambda: OpportunityApp.query.get('a2'),
      lambda r: r.resume and r.resume.resume == '{"test":"snapshotnew"}',
      )

    ]
)
def test_put(app, url, update, query, test):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    with app.test_client() as client:
        assert query() is not None, "Item to update should exist"
        assert not test(query())
        response = client.put(url, data=json.dumps(update),
                              headers=headers)
        pprint(response.json)
        assert response.status_code == 200
        assert test(query())

def test_put_contact_saves_deleted_skills(app):
    url, update = ('/api/contacts/123/', {'skills': [
          { 'name': 'Python' },
          { 'name': 'Workforce Development' },
      ]})

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    with app.test_client() as client:
        response = client.put(url, data=json.dumps(update),
                              headers=headers)
        pprint(response.json)
        assert response.status_code == 200
        public_health = ContactSkill.query.filter_by(
            skill_id='n1N02ypni69EZg0SggRIIg==',
            contact_id=123).first()
        assert public_health is not None
        assert public_health.deleted


@pytest.mark.parametrize(
    "url,update,query,test",
    [('/api/contacts/123/',
      {'first_name': 'William', 'last_name':'Daly'},
      lambda: Contact.query.get(123),
      lambda e: len(e.skills) == len(SKILLS['billy']),
      )
    ,('/api/experiences/513/',
      {'host': 'Test'},
      lambda: Experience.query.get(513),
      lambda e: len(e.achievements) == len(EXPERIENCES['baltimore']['achievements'])
      )
    ,('/api/experiences/513/',
      {'host': 'Test'},
      lambda: Experience.query.get(513),
      lambda e: len(e.skills) == len(EXPERIENCES['baltimore']['skills'])
      )
    ])
def test_put_preserves_list_fields(app, url, update, query, test):
    from models.resume_section_model import ResumeSectionSchema
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    with app.test_client() as client:
        assert query() is not None, "Item to update should exist"
        response = client.put(url, data=json.dumps(update),
                              headers=headers)
        pprint(response.json)
        assert response.status_code == 200
        assert test(query())

def test_put_update_achievement_skills(app):
    from models.resume_section_model import ResumeSectionSchema
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    url = '/api/experiences/513/'
    update = {
        'achievements':
              EXPERIENCES['baltimore']['achievements'][0:2] + [{
                  'id': 83,
                  'description': 'Developed recruitment projection tools to model and track progress to goals.',
                  'skills': [{'name': 'Python', 'capability_id': 'cap:it'}],
              }],
        # Achievement skills should add to experience level skills
        'skills': [],
    }
    query = lambda: Experience.query.get(513)
    test = lambda e: (len(e.achievements[-1].skills) == 1
                      and e.achievements[-1].skills[0]['name'] == 'Python')
    with app.test_client() as client:
        assert query() is not None, "Item to update should exist"
        assert not test(query())
        response = client.put(url, data=json.dumps(update),
                              headers=headers)
        pprint(response.json)
        assert response.status_code == 200
        data = response.json['data']
        assert data['achievements'][-1]['skills'][0]['name'] == 'Python'
        assert data['achievements'][-1]['skills'][0]['capability_id'] == 'cap:it'
        exp = query()
        assert test(exp)
        skill_names = {skill.name for skill in exp.skills}
        assert 'Python' in skill_names


def test_contact_put_preserves_experience_skills(app):
    from models.resume_section_model import ResumeSectionSchema
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    update = { 'skills': EXPERIENCES['baltimore']['skills'] }
    with app.test_client() as client:
        response = client.put('/api/contacts/123/', data=json.dumps(update),
                              headers=headers)
        assert response.status_code == 200

        e = Experience.query.get(513)
        assert len(e.skills) == len(EXPERIENCES['baltimore']['skills'])

@pytest.mark.parametrize(
    "url,update,old_id,new_id",
    [('/api/contacts/123/',
      {'id': 111, 'first_name': 'test'},
      lambda: Contact.query.get(123),
      lambda: Contact.query.get(111),
      ),
     ('/api/experiences/512/',
      {'id': 555, 'host': 'test'},
      lambda: Experience.query.get(512),
      lambda: Experience.query.get(555),
      )
    ,('/api/contacts/123/programs/1/',
      {'id': 555, 'stage': 2},
      lambda: ProgramContact.query.get(5),
      lambda: ProgramContact.query.get(555),
      )
    ,('/api/opportunity/123abc/',
      {'id': 'aaaaaa', 'title': 'new title'},
      lambda: Opportunity.query.get('123abc'),
      lambda: Opportunity.query.get('aaaaaa'),
      )
    ]
)
def test_put_rejects_id_update(app, url, update, old_id, new_id):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    with app.test_client() as client:
        assert old_id() is not None, "Item to update should exist"
        assert new_id() is None, "New id should not exist before test"
        response = client.put(url, data=json.dumps(update),
                              headers=headers)
        assert response.status_code == 200
        assert old_id() is not None, "Item to update should still exist"
        assert new_id() is None, "New id should not exist after test"

def test_put_rejects_app_stage_update(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    update = {
        'stage': 0,
        'status': 'draft',
    }
    with app.test_client() as client:
        response = client.put('/api/contacts/123/app/123abc/',
                              data=json.dumps(update),
                              headers=headers)
        assert OpportunityApp.query.get('a1').stage == ApplicationStage.submitted.value

def test_opportunity_app_submit(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    update = {}
    with app.test_client() as client:
        assert OpportunityApp.query.get('a2').stage == ApplicationStage.draft.value
        response = client.post('/api/contacts/123/app/222abc/submit/',
                              data=json.dumps(update),
                              headers=headers)
        assert response.status_code == 200
        assert OpportunityApp.query.get('a2').stage == ApplicationStage.submitted.value


@pytest.mark.parametrize(
    "delete_url,query",
    [('/api/contacts/123?token=testing_token',
      lambda: Contact.query.get(123))
    ,('/api/experiences/512/', lambda: Experience.query.get(512))
    ,('/api/contacts/123/skills/n1N02ypni69EZg0SggRIIg==',
      lambda: ContactSkill.query.filter_by(
          skill_id='n1N02ypni69EZg0SggRIIg==', contact_id=123, deleted=False).first())
    ,('/api/contacts/123/capabilities/cap:it/suggestion/QUEVjv1tcq6uLmzCku6ikg==',
      lambda: CapabilitySkillSuggestion.query.get(
          (123, 'cap:it', 'QUEVjv1tcq6uLmzCku6ikg=='))
      )
    ]

)
def test_delete(app, delete_url, query):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    with app.test_client() as client:
        assert query() is not None, "Item to delete should exist"

        response = client.delete(delete_url, headers=headers)
        assert response.status_code == 200
        assert query() is None, "Deleted item should not exist"


def test_delete_contact_skill_saved(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    delete_url = '/api/contacts/123/skills/n1N02ypni69EZg0SggRIIg=='
    with app.test_client() as client:
        response = client.delete(delete_url, headers=headers)
        assert response.status_code == 200
        contact_skill = ContactSkill.query.filter_by(
            skill_id='n1N02ypni69EZg0SggRIIg==', contact_id=123).first()
        assert contact_skill is not None
        assert contact_skill.deleted


@pytest.mark.parametrize(
    "url,expected",
    [('/api/contacts/123/', CONTACTS['billy'])
    ,('/api/contacts/124/', CONTACTS['obama'])
    ,('/api/experiences/512/', EXPERIENCES['goucher'])
    ,('/api/experiences/513/', EXPERIENCES['baltimore'])
    ,('/api/contacts/123/skills', SKILLS['billy'])
    ,('/api/contacts/123/programs/1', PROGRAM_CONTACTS['billy_pfp'])
    ,('/api/opportunity/123abc', OPPORTUNITIES['test_opp1'])
    ,('/api/contacts/123/app/123abc', APPLICATIONS['app_billy'])
    ]
)
def test_get(app, url, expected):
    #the expected data comes from the EXPERIENCES constant above
    #the actual data come from the populate_db.py script
    #in the common directory
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    with app.test_client() as client:
        response = client.get(url, headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)['data']
        assert len(data) > 0
        assert data == expected


def test_get_autocomplete(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    query = {
        'q': 'Pyt',
    }
    with app.test_client() as client:
        response = client.get('/api/skills/autocomplete/',
                              query_string=query, headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)['data']
        assert len(data) > 0
        assert 'matches' in data
        assert 'got_exact' in data
        assert 'Python' in data['matches']

def test_get_capability_recommendations(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    expected = {
        'Advocacy and Public Policy': [
            'Community Organizing',
            'Canvassing',
            'Advocacy',
            'Policy Writing',
            'Volunteer Mobilization',
        ],
        'Community Engagement and Outreach': [
            'Community Engagement',
            'Client Recruitment',
            'Partnership Building',
            'Event Planning',
            'Community Organizing',
        ],
        'Information Technology': [],
    }
    with app.test_client() as client:
        response = client.get('/api/capabilities/',
                              headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)['data']
        pprint(data)
        for capability in data:
            assert capability['name'] in expected
            for i, skill in enumerate(capability['recommended_skills']):
                skill['skill']['name'] == expected[capability['name']][i]

@pytest.mark.parametrize(
    "url,expected",
    [('/api/contacts/', CONTACTS.values())
    ,('/api/contacts/123/experiences/', [EXPERIENCES['goucher'],
                                         EXPERIENCES['baltimore']])
    ,('/api/contacts/124/experiences/', [EXPERIENCES['columbia']])
    ,('/api/contacts/123/achievements/', ACHIEVEMENTS.values())
    ,('/api/contacts/123/programs/', [PROGRAM_CONTACTS['billy_pfp']])
    ,('/api/opportunity/', OPPORTUNITIES.values())
    ,('/api/contacts/123/app/', [APPLICATIONS['app_billy']])
    ]
)
def test_get_many_unordered(app, url, expected):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    with app.test_client() as client:
        response = client.get(url, headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)['data']

        # Test that the data and expected contain the same items, but not
        # necessarily in the same order
        assert len(data) == len(expected)
        pprint(list(expected))
        for item in data:
            pprint(item)
            assert item in expected

def test_get_contact_capabilities(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    url, expected = ('/api/contacts/123/capabilities/', CAPABILITIES['billy'])
    with app.test_client() as client:
        response = client.get(url, headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)['data']

        pprint(expected)
        pprint(data)
        assert data == expected


@pytest.mark.skip
@pytest.mark.parametrize(
    "url,input,output",
    [('/api/contacts/123/generate-resume/',POSTS['resume'],RESUME_OUTPUT)]
)
def test_generate_resume(app, url, input, output):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    with app.test_client() as client:
        response = client.post(url, data=json.dumps(input),
                               headers=headers)
        pprint(response.json)
        assert response.status_code == 201
        data = json.loads(response.data)['data']
        assert len(data) > 0
        assert data == output


def make_session(contact_id, permissions=[]):
    return UserSession(
        id="fake_session_id",
        auth_id="fake_auth_id",
        contact_id=contact_id,
        jwt=json.dumps({'permissions': permissions}),
        expiration=(dt.datetime.utcnow() + dt.timedelta(days=1)),
    )

@pytest.mark.parametrize(
    "method,url,data,successes,failures",
    [pytest.param(
        'POST',
        '/api/opportunity/',
      POSTS['opportunity'],
      [make_session(1, ['write:opportunity'])],
      [make_session(1)],
      marks=pytest.mark.skip)
    ]
)
def test_authz(app, method, url, data, successes, failures):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'X-Test-Authz': '1',
    }

    for success in successes:
        with app.test_client() as client:
            g.test_user = success
            client_method = getattr(client, method.lower())
            response = client_method(url, data=json.dumps(data), headers=headers)
            assert response.status_code != 401

    for failure in failures:
        with app.test_client() as client:
            g.test_user = failure
            client_method = getattr(client, method.lower())
            response = client_method(url, data=json.dumps(data), headers=headers)
            assert response.status_code == 401

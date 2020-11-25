import json
import datetime as dt
from pprint import pprint
import pytest
import math
import copy

from models.base_model import db
from models.contact_model import Contact, ContactStage
from models.experience_model import Experience, Month, Type as ExpType
from models.session_model import UserSession
from models.opportunity_model import Opportunity
from models.opportunity_app_model import OpportunityApp, ApplicationStage
from models.profile_model import Profile

from models.skill_model import (
    CapabilitySkillSuggestion
)
from models.skill_item_model import (
    ContactSkill,
    ExperienceSkill,
    AchievementSkill,
)

from flask import g

from tests.contact.contact_data import CONTACTS_API, INSTRUCTIONS_API, EMAILS_API
from tests.opportunity.opportunity_data import OPPS_API, OPP_APPS_API, OPPS_INTERNAL_API
from tests.skill.skill_data import CONTACT_SKILLS, CAPABILITIES_API
from tests.profile.profile_data import PROFILES_API
from tests.experience.experience_data import EXPERIENCES_API, ACHIEVEMENTS_API
from tests.program.program_data import PROGRAMS_API, PROGRAM_APPS_API



POSTS = {
    'experience': {
        'description': 'Test description',
        'host': 'Test Org',
        'title': 'Test title',
        'start_month': 'September',
        'start_year': 2000,
        'end_month': 'May',
        'end_year': 2019,
        'link': None,
        'link_name': None,
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
    'opportunity': {
        "title": "Test Opportunity",
        "short_description": "We are looking for a tester to test our application by taking this test opportunity. Testers of all experience welcome",
        "gdoc_id": "TESTABC11==",
        "cycle_id": 1,
        "org_name": 'Test Org',
        "gdoc_link": "https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit",
        "is_active": True,
        'program_name': "Place for Purpose"
    },
    'mayoral_opportunity': {
        "title": "Mayoral Test 1",
        "short_description": "We are looking for a tester to test our application by taking this test opportunity. Testers of all experience welcome",
        "gdoc_id": "TESTABC11==",
        "org_name": 'Test Org',
        "gdoc_link": "https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit",
        "is_active": True,
        'program_name': "Mayoral Fellowship"
    },
    'blank_opportunity': {
        "title": "Blank Test 1",
        "short_description": "We are looking for a tester to test our application by taking this test opportunity. Testers of all experience welcome",
        "gdoc_id": "TESTABC11==",
        "org_name": 'Test Org',
        "gdoc_link": "https://docs.google.com/document/d/19Xl2v69Fr2n8iTig4Do9l9BUvTqAwkJY87_fZiDIs4Q/edit",
        "is_active": True,
        'program_name': None,
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
    [('/api/contacts/123/experiences/',
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


def test_post_experience_date(app):
    id_, _ = post_request(app, '/api/contacts/123/experiences/',
                          POSTS['experience'])
    assert Experience.query.get(id_).end_month == Month.may
    assert Experience.query.get(id_).end_year == 2019
    assert Experience.query.get(id_).start_month == Month.september
    assert Experience.query.get(id_).start_year == 2000


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

        data = response.json['data']
        assert data['contact'].get('profile', None) is None

        assert UserSession.query.filter_by(contact_id=123).first().contact.first_name == 'Billy'

def test_get_session(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': 'Bearer test-valid|0123456789abcdefabcdefff',
    }

    with app.test_client() as client:

        # set email to null
        contact = Contact.query.get(123)
        contact.email = None
        db.session.commit()

        # confirm it was set to null
        contact = Contact.query.get(123)
        assert contact.email is None

        # create session then query it
        client.post('/api/session/', headers=headers)
        response = client.get('/api/session/', headers=headers)
        assert response.status_code == 200
        data = response.json['data']
        pprint(data)
        assert data['contact']['email'] == 'billy@example.com'
        assert UserSession.query.filter_by(contact_id=123).first().contact.first_name == 'Billy'

def skill_name(skill):
    return skill.name

@pytest.mark.parametrize(
    "url,update,query,test",
    [('/api/experiences/512/',
      {'end_month': 'January', 'end_year': 2017},
      lambda: Experience.query.get(512),
      lambda e: e.end_month == Month.january and e.end_year == 2017,
      )
    ,('/api/experiences/512/',
      {'achievements': EXPERIENCES_API['billy_edu']['achievements'] + [
          {'description': 'test'}
      ]},
      lambda: Experience.query.get(512),
      lambda e: e.achievements[-1].description == 'test',
      )
    ,('/api/experiences/513/',
      {'achievements': EXPERIENCES_API['billy_work']['achievements'][0:2] + [{
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
      {'achievements': EXPERIENCES_API['billy_work']['achievements'][0:2] + [{
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
      {'skills': CONTACT_SKILLS['billy'][0:2] + [{'name': 'Test'}]},
      lambda: Experience.query.get(513),
      lambda e: (len(e.skills) == 3
                 and sorted(e.skills, key=skill_name)[0].name == 'Community Organizing'
                 and sorted(e.skills, key=skill_name)[1].name == 'Flask'
                 and sorted(e.skills, key=skill_name)[2].name == 'Test'),
      )]
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

def test_put_program_apps_new(app):
    url = '/api/contacts/124/program-apps/interested'
    update = PROGRAM_APPS_API['obama']

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    obama = Contact.query.get(124)
    assert obama.program_apps == []

    with app.test_client() as client:
        response = client.put(url, data=json.dumps(update),
                              headers=headers)
        pprint(response.json)
        assert response.status_code == 200
        data = response.json['data']
        assert data == PROGRAM_APPS_API['obama']

def test_put_program_apps_update(app):
    url = '/api/contacts/123/program-apps/interested'
    update = copy.deepcopy(PROGRAM_APPS_API['billy'])
    update['program_apps'][0]['is_interested'] = False
    update['program_apps'][1]['is_interested'] = True

    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    billy = Contact.query.get(123)
    assert billy.program_apps[0].is_interested == True
    assert billy.program_apps[1].is_interested == False

    with app.test_client() as client:
        response = client.put(url, data=json.dumps(update),
                              headers=headers)
        pprint(response.json)
        assert response.status_code == 200
        data = response.json['data']
        billy = Contact.query.get(123)
        assert billy.program_apps[0].is_interested == False
        assert billy.program_apps[1].is_interested == True


@pytest.mark.parametrize(
    "url,update,query,test",
    [('/api/contacts/123/',
      {'first_name': 'William', 'last_name':'Daly'},
      lambda: Contact.query.get(123),
      lambda e: len(e.skills) == len(CONTACT_SKILLS['billy']),
      )
    ,('/api/experiences/513/',
      {'host': 'Test'},
      lambda: Experience.query.get(513),
      lambda e: len(e.achievements) == len(EXPERIENCES_API['billy_work']['achievements'])
      )
    ,('/api/experiences/513/',
      {'host': 'Test'},
      lambda: Experience.query.get(513),
      lambda e: len(e.skills) == len(EXPERIENCES_API['billy_work']['skills'])
      )
    ])
def test_put_preserves_list_fields(app, url, update, query, test):
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
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    url = '/api/experiences/513/'
    update = {
        'achievements':
              EXPERIENCES_API['billy_work']['achievements'][0:2] + [{
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
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    update = { 'skills': EXPERIENCES_API['billy_work']['skills'] }
    with app.test_client() as client:
        response = client.put('/api/contacts/123/', data=json.dumps(update),
                              headers=headers)
        assert response.status_code == 200

        e = Experience.query.get(513)
        assert len(e.skills) == len(EXPERIENCES_API['billy_work']['skills'])

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


def test_opportunity_app_interview_completed_property(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    with app.test_client() as client:
        opp_app = OpportunityApp.query.get('a1')
        assert  opp_app.interview_completed == False

        # set interview to a scheduled date
        now = dt.datetime.now()
        scheduled = now + dt.timedelta(hours=1)
        completed = now - dt.timedelta(hours=1)
        opp_app.interview_date = scheduled.date()
        opp_app.interview_time = scheduled.strftime('%H:%M:%S')
        db.session.commit()

        # test that interview fields were set
        # and that interview_completed == False
        opp_app = OpportunityApp.query.get('a1')
        assert opp_app.interview_date == scheduled.date()
        assert opp_app.interview_time == scheduled.strftime('%H:%M:%S')
        assert opp_app.interview_completed == False

        # set interview to a completed date
        opp_app.interview_date = completed.date()
        opp_app.interview_time = completed.strftime('%H:%M:%S')
        db.session.commit()

        # test that interview fields were set
        # and that interview_completed == False
        opp_app = OpportunityApp.query.get('a1')
        assert opp_app.interview_date == completed.date()
        assert opp_app.interview_time == completed.strftime('%H:%M:%S')
        assert opp_app.interview_completed == True

def test_opportunity_app_interview(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    update = {'interview_date': '2050-02-01',
              'interview_time': '13:00:00'}
    with app.test_client() as client:
        assert OpportunityApp.query.get('a1').stage == ApplicationStage.submitted.value
        response = client.post('/api/contacts/123/app/123abc/interview/',
                              data=json.dumps(update),
                              headers=headers)
        assert response.status_code == 200
        opp_app = OpportunityApp.query.get('a1')
        assert opp_app.stage == ApplicationStage.interviewed.value
        assert opp_app.is_active == True
        assert opp_app.interview_date == dt.date(2050,2,1)
        assert opp_app.interview_time == '13:00:00'
        assert opp_app.interview_completed == False

def test_opportunity_app_consider(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    update = {}
    with app.test_client() as client:
        assert OpportunityApp.query.get('a1').stage == ApplicationStage.submitted.value
        response = client.post('/api/contacts/123/app/123abc/consider/',
                              data=json.dumps(update),
                              headers=headers)
        assert response.status_code == 200
        assert OpportunityApp.query.get('a1').stage == ApplicationStage.considered_for_role.value
        assert OpportunityApp.query.get('a1').is_active == True

def test_opportunity_app_recommend_from_not_a_fit(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    update = {}
    with app.test_client() as client:
        OpportunityApp.query.get('a1').is_active = False
        db.session.commit()
        opp_app = OpportunityApp.query.get('a1')
        assert opp_app.stage == ApplicationStage.submitted.value
        assert opp_app.is_active == False
        response = client.post('/api/contacts/123/app/123abc/recommend/',
                              data=json.dumps(update),
                              headers=headers)
        assert response.status_code == 200
        opp_app = OpportunityApp.query.get('a1')
        assert opp_app.stage == ApplicationStage.recommended.value
        assert opp_app.is_active == True

def test_opportunity_app_recommend(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    update = {}
    with app.test_client() as client:
        assert OpportunityApp.query.get('a1').stage == ApplicationStage.submitted.value
        response = client.post('/api/contacts/123/app/123abc/recommend/',
                              data=json.dumps(update),
                              headers=headers)
        assert response.status_code == 200
        assert OpportunityApp.query.get('a1').stage == ApplicationStage.recommended.value

def test_opportunity_app_reopen(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    update = {}
    with app.test_client() as client:
        assert OpportunityApp.query.get('a1').stage == ApplicationStage.submitted.value
        response = client.post('/api/contacts/123/app/123abc/reopen/',
                              data=json.dumps(update),
                              headers=headers)
        assert response.status_code == 200
        assert OpportunityApp.query.get('a1').stage == ApplicationStage.draft.value




@pytest.mark.parametrize(
    "delete_url,query",
    [('/api/experiences/512/', lambda: Experience.query.get(512))
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
    [('/api/experiences/512/', EXPERIENCES_API['billy_edu'])
    ,('/api/experiences/513/', EXPERIENCES_API['billy_work'])
    ,('/api/contacts/123/skills', CONTACT_SKILLS['billy'])
    ,('/api/contacts/123/app/123abc', OPP_APPS_API['billy1'])
    ,('/api/contacts/123/about-me', PROFILES_API['billy'])
    ,('/api/contacts/123/program-apps', PROGRAM_APPS_API['billy'])
    ,('/api/contacts/123/instructions', INSTRUCTIONS_API['billy'])
    ,('/api/contacts/124/instructions', INSTRUCTIONS_API['obama'])
    ,('/api/org/opportunities/123abc', OPPS_INTERNAL_API['opp1'])
    ,('/api/contacts/123/program-apps', PROGRAM_APPS_API['billy'])]
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
        pprint(data)
        pprint(expected)
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
    [('/api/contacts/123/experiences/', [EXPERIENCES_API['billy_edu'],
                                         EXPERIENCES_API['billy_work']])
    ,('/api/contacts/124/experiences/', [EXPERIENCES_API['obama_portfolio']])
    ,('/api/contacts/123/app/', [OPP_APPS_API['billy1']])
    ,('/api/contacts/program-apps/?is_approved=true', [PROGRAM_APPS_API['billy']])
    ,('/api/contacts/program-apps/?is_approved=false', [PROGRAM_APPS_API['obama_none']])
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
        print('EXPECTED')
        pprint(list(expected))
        print('DATA')
        pprint(data)
        assert len(data) == len(expected)
        for item in data:
            pprint(item)
            assert item in expected

def test_get_contact_capabilities(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    url, expected = ('/api/contacts/123/capabilities/', CAPABILITIES_API['billy'])
    with app.test_client() as client:
        response = client.get(url, headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)['data']

        pprint(expected)
        pprint(data)
        assert data == expected

def test_get_contact_status_query(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    with app.test_client() as client:

        # checks approved
        response = client.get('/api/contacts/?status=approved',
                              headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)['data']
        assert data == [CONTACTS_API['billy']]

        # checks created
        response = client.get('/api/contacts/?status=created',
                              headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)['data']
        assert data == [CONTACTS_API['obama']]

        # sets obama to submitted
        obama = Contact.query.get(124)
        obama.stage = 2
        db.session.commit()
        obama = Contact.query.get(124)
        assert obama.status == ContactStage(2)
        expected = copy.deepcopy([CONTACTS_API['obama']])
        expected[0]['status'] = 'submitted'

        # checks submitted
        response = client.get('/api/contacts/?status=submitted',
                              headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)['data']
        assert data == expected

@pytest.mark.skip
def test_get_contact_without_apps(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    url, expected = ('/api/contacts/124/app/', [])
    with app.test_client() as client:

        response = client.get(url, headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)['data']

        pprint(expected)
        pprint(data)
        assert data == expected


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

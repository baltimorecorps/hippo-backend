import json
from datetime import date
from pprint import pprint
from models.contact_model import Contact
from models.experience_model import Experience
from models.resume_model import Resume
from models.resume_section_model import ResumeSection
from models.tag_model import Tag
from models.tag_item_model import TagItem
import pytest

"""
* GET api/contacts/
* GET api/contacts/<int:contact_id>/
* GET api/contacts/<contact_id>/experiences/
* GET api/experiences/<int:exp_id>/
* GET api/tags/
* GET api/tags/<tag_id>/
* GET api/contacts/<int:contact_id>/achievements/
* GET api/contacts/<contact_id>/tags/
* GET api/contact/<contact_id>/resumes/
* GET api/resumes/<int:resume_id>/
* GET api/resumes/<resume_id>/sections/
* GET api/resumes/<resume_id>/sections/<section_id>/

* POST api/contacts/
POST api/contacts/<contact_id>/experiences/
POST api/tags/
POST api/contacts/<contact_id>/tags/
POST api/contacts/<contact_id>/resumes/
POST api/resumes/<resume_id>/sections/<section_id>/

* PUT api/experiences/<int:exp_id>/
* PUT api/contacts/<contact_id>/tags/<tag_id>/
* PUT api/resumes/<resume_id>/
* PUT api/resumes/<resume_id>/sections/<section_id>/

* DELETE api/experiences/<int:exp_id>/
* DELETE api/resumes/<resume_id>/
* DELETE api/resumes/<int:section_id>/sections/<section_id>/
"""

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
        'birthdate': '1991-01-02',
        'phone_primary': "555-245-2351",
        'race_all': "White",
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
        'birthdate': '1961-08-04',
        'phone_primary': "555-444-4444",
        'race_all': "Black",
    },
}

ACHIEVEMENTS = {
    'baltimore1': {
        'id': 81,
        'description': 'Redesigned the Salesforce architecture to facilitate easier reporting.',
    },
    'baltimore2': {
        'id': 82,
        'description': 'Formalized organizational strategy for defining and analyzing KPIs.',
    },
    'baltimore3': {
        'id': 83,
        'description': 'Developed recruitment projection tools to model and track progress to goals.',
    },
    'goucher1': {
        'id': 84,
        'description': 'Did some stuff',
    }
}

EXPERIENCES = {
    'columbia': {
        'id': 511,
        'description': None,
        'host': 'Columbia University',
        'title': 'Political Science',
        'degree': 'Undergraduate',
        'date_start': '1979-09-03',
        'date_end': '1983-05-22',
        'type': 'Education',
        'contact_id': 124,
        'achievements': [],
    },
    'goucher': {
        'id': 512,
        'description': None,
        'host': 'Goucher College',
        'title': 'Economics',
        'degree': 'Undergraduate',
        'date_start': '2012-09-01',
        'date_end': '2016-05-20',
        'type': 'Education',
        'contact_id': 123,
        'achievements': [
            ACHIEVEMENTS['goucher1'],
        ],
    },
    'baltimore' : {
        'id': 513,
        'description': 'Test description here',
        'host': 'Baltimore Corps',
        'title': 'Systems Design Manager',
        'degree': 'Undergraduate',
        'date_start': '2000-01-01',
        'date_end': '2019-07-17',
        'type': 'Work',
        'contact_id': 123,
        'achievements': [
            ACHIEVEMENTS['baltimore1'],
            ACHIEVEMENTS['baltimore2'],
            ACHIEVEMENTS['baltimore3'],
        ],
    },
}

TAGS = {
    'python': {
        'id': 123,
        'name': 'Python',
        'type': 'Skill',
    },
    'webdev': {
        'id': 124,
        'name': 'Web Development',
        'type': 'Function',
    },
    'health': {
        'id': 125,
        'name': 'Public Health',
        'type': 'Topic',
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
        'sections': [
            filter_dict(RESUME_SECTIONS['billy_work'], {'resume_id'}),
            filter_dict(RESUME_SECTIONS['billy_skills'], {'resume_id'}),
        ],
    },
}



@pytest.mark.parametrize(
    "url,data,query",
    [('/api/contacts/', 
      {
          "first_name": "Tester",
          "last_name": "Byte",
          "email_primary": {
              "email": "testerb@example.com",
              "is_primary": True, 
          },
          "phone_primary": "111-111-1111",
          "gender": "Female",
          "race_all": "Hispanic/Latino",
          "birthdate": "1973-04-23",
      },
      lambda id: Contact.query.get(id)
      )
    ,('/api/contacts/123/experiences/', 
      {
          'description': 'Test description',
          'host': 'Test Org',
          'title': 'Test title',
          'date_start': '1910-09-03',
          'date_end': '2019-05-22',
          'type': 'Work',
          'contact_id': 123,
          'achievements': [
              {'description': 'Test achievement 1'},
              {'description': 'Test achievement 2'},
          ],
      },
      lambda id: Experience.query.get(id)
      )
    ,('/api/tags/', 
      {
          'name': 'Test Tag',
          'type': 'Skill',
      },
      lambda id: Tag.query.get(id)
      )
    ,('/api/contacts/123/tags/', 
      {
        'contact_id': 123,
        'tag_id': 125,
        'score': 4,
      },
      lambda id: TagItem.query.get(id)
      )
    ,('/api/contacts/123/resumes/', 
      {
        'contact_id': 123,
        'name': 'Test Resume',
        'date_created': '2019-01-01',
      },
      lambda id: Resume.query.get(id)
      )
    ,('/api/resumes/51/sections/', 
      {
        'resume_id': 51,
        'min_count': 1,
        'max_count': 50,
        'name': "Test Section",
        'items': [
            {
                'resume_order': 0,
                'indented': False,
                'experience_id': 512,
            },
        ],
      },
      lambda id: ResumeSection.query.get(id)
      )
    ]
)
def test_post(app, url, data, query):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    with app.test_client() as client:
        response = client.post(url, data=json.dumps(data), headers=headers)
        pprint(response.json)
        assert response.status_code == 201
        data = json.loads(response.data)['data']
        assert len(data) > 0
        assert data['id'] is not None
        id = data['id']
        assert query(data['id']) is not None

@pytest.mark.parametrize(
    "url,update,query,test",
    [('/api/experiences/512/', 
      {'date_end': '2017-01-01'},
      lambda: Experience.query.get(512),
      lambda e: e.date_end == date(2017, 1, 1),
      )
    ,('/api/experiences/512/', 
      {'achievements': EXPERIENCES['goucher']['achievements'] + [
          {'description': 'test'} 
      ]},
      lambda: Experience.query.get(512),
      lambda e: e.achievements[-1].description == 'test',
      )
    ,('/api/contacts/123/tags/124/',
      {'score': 3},
      lambda: TagItem.query.get(21),
      lambda ti: ti.score == 3,
      )
    ,('/api/resumes/51/',
      {'name': 'test'},
      lambda: Resume.query.get(51),
      lambda r: r.name == 'test',
      )
    ,('/api/resumes/51/sections/61/',
      {'items': [{
          'resume_order': 0,
          'indented': True,
          'achievement_id': 81,
      }]},
      lambda: ResumeSection.query.get(61),
      lambda rs: (len(rs.items) == 1 
                  and rs.items[0].achievement is not None 
                  and rs.items[0].achievement.description == 
                      ACHIEVEMENTS['baltimore1']['description'])
      )
    ]
)
def test_put(app, url, update, query, test):
    from models.resume_section_model import ResumeSectionSchema
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
        print(response.json)
        assert response.status_code == 200
        assert test(query())


@pytest.mark.parametrize(
    "delete_url,query",
    [('/api/experiences/512/', lambda: Experience.query.get(512))
    ,('/api/resumes/51/', lambda: Resume.query.get(51))
    ,('/api/resumes/51/sections/61/', lambda: ResumeSection.query.get(61))
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


@pytest.mark.parametrize(
    "url,expected",
    [('/api/contacts/123/', CONTACTS['billy'])
    ,('/api/contacts/124/', CONTACTS['obama'])
    ,('/api/experiences/512/', EXPERIENCES['goucher'])
    ,('/api/experiences/513/', EXPERIENCES['baltimore'])
    ,('/api/tags/123/', TAGS['python'])
    ,('/api/tags/124/', TAGS['webdev'])
    ,('/api/resumes/51/', RESUMES['billy'])
    ,('/api/resumes/51/sections/61/', RESUME_SECTIONS['billy_work'])
    ]
)
def test_get(app, url, expected):
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

@pytest.mark.parametrize(
    "url,expected",
    [('/api/contacts/', CONTACTS.values())
    ,('/api/contacts/123/experiences/', [EXPERIENCES['goucher'], 
                                         EXPERIENCES['baltimore']])
    ,('/api/contacts/124/experiences/', [EXPERIENCES['columbia']])
    ,('/api/contacts/123/achievements/', ACHIEVEMENTS.values())
    ,('/api/tags/', TAGS.values())
    ,('/api/contacts/123/tags/', TAG_ITEMS.values())
    ,('/api/contacts/123/resumes/', RESUMES.values())
    ,('/api/resumes/51/sections/', RESUME_SECTIONS.values())
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


def est_post_one_contact(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        "first_name": "Susan",
        "last_name": "Smith",
        "email_primary": {
            "email": "p@gmail.com",
            "is_primary": True, 
        },
        "phone_primary": "111-111-1111",
        "gender": "Female",
        "race_all": "White",
        "birthdate": "1973-04-23"
    }
    url = '/api/contacts/'
    with app.test_client() as client:
        response = client.post(url, data=json.dumps(data), headers=headers)
        assert response.status_code == 201
        data = json.loads(response.data)['data']
        assert len(data) > 0
        assert data['id'] is not None

        response = client.get(url + str(data['id']) + '/')
        assert response.status_code == 200
        print(json.loads(response.data))
        assert true == false

#
def est_post_one_experience(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    exp_data = {
        "description": "Tutored after-school",
        "host": "BPL",
        "title": "Volunteer",
        "date_start": "2000-01-01",
        "date_end": "2010-01-01",
        "type": "Service"
    }
    contact_data = {
        "first_name": "Susan",
        "last_name": "Smith",
        # "email_primary": "p@gmail.com",
        "phone_primary": "111-111-1111",
        "gender": "Female",
        "race_all": "White",
        "birthdate": "1973-04-23"
    }
    contact_url = '/api/contacts/'
    with app.test_client() as client:
        # add contact
        response = client.post(contact_url, data=json.dumps(contact_data), headers=headers)
        assert response.status_code == 201
        contact_id = json.loads(response.data)['data']['id']
        exp_url = contact_url + str(contact_id) + '/experiences/'
        response = client.get(exp_url)
        # assert experience list is empty
        assert len(json.loads(response.data)['data']) == 0
        # add experience to that contact using contact_id
        response = client.post(exp_url, data=json.dumps(exp_data), headers=headers)
        assert response.status_code == 201
        response = client.get(exp_url)
        # assert experience list is not empty
        data = json.loads(response.data)['data']
        assert len(data) > 0
        assert data[0]['id'] is not None

def est_put_by_experience_id(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    exp_data = {
        "description": "Tutored after-school",
        "host": "BPL",
        "title": "Volunteer",
        "date_start": "2000-01-01",
        "date_end": "2010-01-01",
        "type": "Service"
    }
    contact_data = {
        "first_name": "Susan",
        "last_name": "Smith",
        # "email_primary": "p@gmail.com",
        "phone_primary": "111-111-1111",
        "gender": "Female",
        "race_all": "White",
        "birthdate": "1973-04-23"
    }
    update_data = {
        "type": "Work"
    }
    contact_url = '/api/contacts/'
    with app.test_client() as client:
        #add contact to db
        response = client.post(contact_url, data=json.dumps(contact_data), headers=headers)
        assert response.status_code == 201
        contact_id = json.loads(response.data)['data']['id']
        exp_url = contact_url + str(contact_id) + '/experiences/'
        #add experience to that contact using contact_id
        response = client.post(exp_url, data=json.dumps(exp_data), headers=headers)
        assert response.status_code == 201
        data = json.loads(response.data)['data']
        assert data['type'] == "Service"
        exp_id = data['id']
        upd_url = exp_url + str(exp_id)
        #update that experience using exp_id
        response = client.put(upd_url, data=json.dumps(update_data), headers=headers)
        assert response.status_code == 201
        #check that it was updated properly
        response = client.get(upd_url)
        assert response.status_code == 200
        assert json.loads(response.data)['data']['type'] == "Work"

def est_get_contact_profile(app):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        "first_name": "Amy",
        "last_name": "Smith",
        # "email_primary": "amy@yahoo.com",
        "phone_primary": "401-234-1124",
        "gender": "Female",
        "race_all": "White",
        "birthdate": "1983-02-09"
    }
    url = '/api/contacts/'
    with app.test_client() as client:
        # add contact
        response = client.post(url, data=json.dumps(data), headers=headers)
        assert response.status_code == 201
        data = json.loads(response.data)['data']
        id = data['id']
        profile_url = url + str(id) + "/profile"
        # check that a profile exists
        response = client.get(profile_url)
        assert response.status_code == 200
        data = json.loads(response.data)['data']
        assert len(data) > 0
        assert data['service_experience'] is not None



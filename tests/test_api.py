import json
import datetime as dt
from pprint import pprint
import pytest
import math

from models.contact_model import Contact
from models.experience_model import Experience, Month
from models.resume_model import Resume
from models.resume_section_model import ResumeSection
from models.tag_model import Tag
from models.tag_item_model import TagItem

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

DATE_START = dt.date(2000, 1, 1)
DATE_END = dt.datetime.today()
DATE_LENGTH = ((DATE_END.year - DATE_START.year) * 12
               + DATE_END.month - DATE_START.month)

EXPERIENCES = {
    'columbia': {
        'id': 511,
        'description': None,
        'host': 'Columbia University',
        'title': 'Political Science',
        'degree': 'Undergraduate',
        'is_current': False,
        'start_month': 'September',
        'start_year': 1979,
        'end_month': 'May',
        'end_year': 1983,
        'length_year': 3,
        'length_month': 8,
        'type': 'Education',
        'contact_id': 124,
        'location_city': 'New York',
        'location_state': 'New York',
        'achievements': [],
    },
    'goucher': {
        'id': 512,
        'description': None,
        'host': 'Goucher College',
        'title': 'Economics',
        'degree': 'Undergraduate',
        'is_current': False,
        'start_month': 'September',
        'start_year': 2012,
        'end_month': 'May',
        'end_year': 2016,
        'length_year': 3,
        'length_month': 8,
        'type': 'Education',
        'contact_id': 123,
        'location_city': 'Towson',
        'location_state': 'Maryland',
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
        'is_current': True,
        'start_month': 'January',
        'start_year': 2000,
        'end_month': None,
        'end_year': None,
        'length_year': math.floor(DATE_LENGTH/12),
        'length_month': DATE_LENGTH % 12,
        'type': 'Work',
        'contact_id': 123,
        'location_city': 'Baltimore',
        'location_state': 'Maryland',
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
        'sections': [
            filter_dict(RESUME_SECTIONS['billy_work'], {'resume_id'}),
            filter_dict(RESUME_SECTIONS['billy_skills'], {'resume_id'}),
        ],
    },
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
        'location_city': 'Test City',
        'location_state': 'Test State',
        'achievements': [
            {'description': 'Test achievement 1'},
            {'description': 'Test achievement 2'},
        ],
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
        return id


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
      POSTS['experience'],
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

    id_ = post_request(app, url, data)
    assert query(id_) is not None


def test_post_experience_date(app):
    id_ = post_request(app, '/api/contacts/123/experiences/',
                          POSTS['experience'])
    assert Experience.query.get(id_).end_month == Month.may
    assert Experience.query.get(id_).end_year == 2019
    assert Experience.query.get(id_).start_month == Month.september
    assert Experience.query.get(id_).start_year == 2000

def test_post_experience_null_degree(app):
    exp = POSTS['experience'].copy()
    exp['degree'] = None
    id_ = post_request(app, '/api/contacts/123/experiences/', exp)
    assert Experience.query.get(id_) is not None
    pprint(Experience.query.get(id_).degree)

def test_post_experience_current(app):
    exp = POSTS['experience'].copy()
    exp['end_month'] = None
    exp['end_'] = None
    id_ = post_request(app, '/api/contacts/123/experiences/', exp)
    assert Experience.query.get(id_) is not None
    assert Experience.query.get(id_).is_current == True


@pytest.mark.parametrize(
    "url,update,query,test",
    [('/api/experiences/512/',
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

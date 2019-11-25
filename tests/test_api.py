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
from models.skill_model import SkillItem

SKILLS = {
    'billy': [
        {
            'id': 'n1N02ypni69EZg0SggRIIg==',
            'name': 'Public Health',
            'contact_id': 123
        },
        {
            'id': '4R9tqGuK2672PavRTJrN_A==',
            'name': 'Python',
            'contact_id': 123
        },
        {
            'id': 'hbBWJS6x6gDxGMUC5HAOYg==',
            'name': 'Web Development',
            'contact_id': 123
        }
    ],
    'obama': [
        {
            'id': 'n1N02ypni69EZg0SggRIIg==',
            'name': 'Public Health',
            'contact_id': 124
        },
    ],
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
        'birthdate': '1991-01-02',
        'phone_primary': "555-245-2351",
        'race_all': "White",
        'account_id': 'billy|123',
        'skills': SKILLS['billy'],
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
        'account_id': None,
        'skills': SKILLS['obama'],
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
        'location': 'New York, NY, USA',
        'achievements': [],
        'skills': [],
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
        'location': 'Towson, MD, USA',
        'achievements': [
            ACHIEVEMENTS['goucher1'],
        ],
        'skills': [],
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
        'skills': SKILLS['billy'][1:3],
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
            {'description': 'Test achievement 2'},
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
    }
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
          "account_id": 'tester|0123456789',
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
    ,('/api/contacts/123/skills',
      {
        'name': 'C++',
      },
      lambda id: SkillItem.query.get(('sEVDZsMOqdfQ-vwoIAEk5A==', 123))
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
    exp['end_month'] = 'none'
    exp['end_year'] = 0
    id_ = post_request(app, '/api/contacts/123/experiences/', exp)
    assert Experience.query.get(id_) is not None
    assert Experience.query.get(id_).is_current == True

def test_post_experience_dump_only(app):
    exp = POSTS['experience'].copy()
    exp['length_year'] = 18
    exp['length_month'] = 8
    exp['is_current'] = False
    exp['id'] = 1
    id_ = post_request(app, '/api/contacts/123/experiences/', exp)
    assert Experience.query.get(id_) is not None

def test_post_experience_skills(app):
    exp = POSTS['experience'].copy()
    exp['skills'] = [{'name': 'C++'}, {'name': 'Python'}]
    id_ = post_request(app, '/api/contacts/123/experiences/', exp)
    assert Experience.query.get(id_).skills[0].name == 'C++'
    assert Experience.query.get(id_).skills[1].name == 'Python'


@pytest.mark.parametrize(
    "url,update,query,test",
    [('/api/contacts/123/',
      {'first_name': 'William', 'last_name':'Daly',
       'gender': None, 'birthdate': None},
      lambda: Contact.query.get(123),
      lambda e: e.first_name == 'William' and e.gender == None,
      ),
     ('/api/contacts/123/',
      {'skills': [
          { 'name': 'Python' }, 
          { 'name': 'Workforce Development' }, 
      ]},
      lambda: Contact.query.get(123),
      lambda e: (len(e.skills) == 2 
                 and e.skills[0].name == 'Python' 
                 and e.skills[1].name == 'Workforce Development'),
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
    ,('/api/experiences/513/',
      {'skills': SKILLS['billy'][0:2] + [{'name': 'Test'}]},
      lambda: Experience.query.get(513),
      lambda e: len(e.skills) == 3 and e.skills[0].name == 'Public Health' and e.skills[-1].name == 'Test',
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
        print(response.json)
        assert response.status_code == 200
        assert test(query())

@pytest.mark.parametrize(
    "delete_url,query",
    [('/api/experiences/512/', lambda: Experience.query.get(512))
    ,('/api/resumes/51/', lambda: Resume.query.get(51))
    ,('/api/contacts/123/skills/n1N02ypni69EZg0SggRIIg==', 
      lambda: SkillItem.query.get(('n1N02ypni69EZg0SggRIIg==', 123)))
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
    ,('/api/contacts/123/skills', SKILLS['billy'])
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

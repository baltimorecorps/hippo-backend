TEST

# Resumer Builder API
## Run on local server

### Getting Started:
- Install Python 3.7

- Clone the repository

- Create virtual environment and activate it

`python3 -m venv`

`source venv/bin/activate`

- Install required python packages

`pip install -r requirements.txt`

- Run the API server 

`python run.py` 

### Using the API

**View all contacts**

URL

```
http://<IP>:5000/api/contacts 
```

Sample call
```
curl --request GET http://127.0.0.1:5000/api/contacts 
```

Output
```
[
    {
        "id": "6",
        "first_name": "Benson",
        "last_name": "Alexander",
        "email": "bensonalexander@zounds.com"
    }
]
```

**View one contact**

URL

```
http://<IP>:5000/api/contacts/<int:contact_id>
```

Sample call
```
curl --request GET http://127.0.0.1:5000/api/contacts/1 
```

Output

```
{
    "status": "success",
    "data": {
        "id": 1,
        "first_name": "Benson",
        "last_name": "Alexander",
        "email": "bensonalexander@zounds.com",
        "phone_primary": "401-111-2222",
        "profile_id": 111,
        "gender": "Male",
        "race_all": "Asian",
        "birthdate": "1990-01-02"
    }
}
```

**View Profile**

URL

```
http://<IP>:5000/api/contacts/<int:contact_id>/profile
```

Sample call

```
curl --request GET http://127.0.0.1:5000/api/contacts/1/profile
```

Output

```
{
    "status": "success",
    "data": {
        "id": "1",
        "first_name": "Amy",
        "last_name": "Smith",
        "email_primary": "amy@yahoo.com",
        "phone_primary": "401-234-1124",
        "current_profile": "11",
        "gender": "Female",
        "race_all": "White",
        "birthdate": "1983-02-09",
        "work_experiences": [
            {
                "id": "1",
                "host": "Kayak",
                "title": "Intern",
                "date_start": "2010-05-25",
                "date_end": "2010-12-13",
                "type": "Intern"
            },
            {
                "id": "2",
                "host": "Wayfair",
                "title": "Software Engineer",
                "date_start": "2011-01-05",
                "date_end": "2011-04-03",
                "type": "SDE"
            }
        ],
        "education_experiences": [
            {
                "id": "3",
                "host": "Brown University",
                "title": "Student",
                "date_start": "2000-09-05",
                "date_end": "2005-05-03",
                "type": "University"
            }
        ],
        "service_experiences": [
            {
                "id": "4",
                "host": "Happy Tails",
                "title": "Volunteer",
                "date_start": "2001-10-19",
                "date_end": "2002-08-13",
                "type": "NGO"
            }
        ],
        "accomplishments": [
            {
                "host": "Brown University",
                "title": "Academic Excellence Award",
                "date": "2003-05-25",
                "type": "Award"
            }
        ],
        "tags": {
            "function_tags": [
                {
                    "id": "1",
                    "name": "abc",
                    "type": "xyz"
                }
            ],
            "skill_tags": [
                {
                    "id": "2",
                    "name": "abc",
                    "type": "xyz"
                }
            ],
            "topic_tags": [
                {
                    "id": "3",
                    "name": "abc",
                    "type": "xyz"
                }
            ]
        }
    }
}
```

**Add contact**

URL
```
http://<IP>:5000/api/contacts
```

Sample call
```
curl --header "Content-Type: application/json" --request POST --data '{"first_name":"abc","last_name": "xyz", "email_primary": "p@gmail.com", "phone_primary":"111-111-1111", "gender": "Female", "race_all": "Asian", "birthdate": "2012-04-23"}' http://127.0.0.1:5000/api/contacts 
```

Output
```
{
    "status": "success",
    "data": {
        "first_name": "abc",
        "last_name": "xyz",
        "email_primary": "p@gmail.com",
        "phone_primary": "111-111-1111",
        "gender": "Female",
        "race_all": "Asian",
        "birthdate": "2012-04-23"
    }
}
```

**View all experiences**

URL
```
http://<IP>:5000/api/contacts/<int:contact_id>/experiences/
```

Sample call
```
curl --request GET http://127.0.0.1:5000/api/contacts/1/experiences/
```

Output
```
{
    "status": "success",
    "data": [
        {
            "id": 0,
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incidi.",
            "host": "ABC",
            "title": "SDE",
            "date_start": "2014-04-03",
            "date_end": "2015-04-03",
            "type": "education"
        },
        {
            "id": 1,
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incidi.",
            "host": "ABC",
            "title": "Accountant",
            "date_start": "2014-04-03",
            "date_end": "2015-04-03",
            "type": "service"
        },
        {
            "id": 2,
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incidi.",
            "host": "ABC",
            "title": "Lawyer",
            "date_start": "2014-04-03",
            "date_end": "2015-04-03",
            "type": "work"
        }
    ]
}

```

**View one experience**

URL
```
http://<IP>:5000/api/contacts/<int:contact_id>/experiences/<int:experience_id>
```

Sample call
```
curl --request GET http://127.0.0.1:5000/api/contacts/1/experiences/2
```

Output
```
{
    "status": "success",
    "data": {
        "id": 2,
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incidi.",
        "host": "ABC",
        "title": "Lawyer",
        "date_start": "2014-04-03",
        "date_end": "2015-04-03",
        "type": "work"
    }
}
```

**Add one experience**

URL
```
http://<IP>:5000/api/contacts/<int:contact_id>/experiences/
```

Sample call
```
curl --header "Content-Type: application/json" --request POST --data '{"description":"hello world hello world hello world hello world", "host": "abc", "title": "xyz", "date_start": "2000-01-01", "date_end":"2010-01-01", "type": "service"}' http://127.0.0.1:5000/api/contacts/1/experiences/
```

Output
```
{
    "status": "success",
    "data": {
        "description": "hello world hello world hello world hello world",
        "host": "abc",
        "title": "xyz",
        "date_start": "2000-01-01",
        "date_end": "2010-01-01",
        "type": "service"
    }
}
```

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
Sample call:

```
curl --request GET http://127.0.0.1:5000/api/contacts
```

**View one contact**

URL

```
http://<IP>:5000/api/contacts/<int:contact_id>
```
Sample call:

```
curl --request GET http://127.0.0.1:5000/api/contacts/1
```

**View Profile**

URL

```
http://<IP>:5000/api/contacts/<int:contact_id>/profile
```

Sample call:

```
curl --request GET http://127.0.0.1:5000/api/contacts/1/profile
```


**Add contact**

URL
```
http://<IP>:5000/api/contacts
```

Sample call:

```
curl --header "Content-Type: application/json" --request POST --data '{"first_name":"abc","last_name": "xyz", "email_primary": "p@gmail.com", "phone_primary":"111-111-1111", "gender": "Female", "race_all": "Asian", "birthdate": "2012-04-23"}' http://127.0.0.1:5000/api/contacts
```

**View all experiences**

URL
```
http://<IP>:5000/api/contacts/<int:contact_id>/experiences/
```

Sample call:

```
curl --request GET http://127.0.0.1:5000/api/contacts/1/experiences/
```

**View one experience**

URL
```
http://<IP>:5000/api/contacts/<int:contact_id>/experiences/<int:experience_id>
```

Sample call:

```
curl --request GET http://127.0.0.1:5000/api/contacts/1/experiences/2
```

**Add one experience**

URL
```
http://<IP>:5000/api/contacts/<int:contact_id>/experiences/
```

Sample call:

```
curl --header "Content-Type: application/json" --request POST --data '{"description":"hello world hello world hello world hello world", "host": "abc", "title": "xyz", "date_start": "2000-01-01", "date_end":"2010-01-01", "type": "service"}' http://127.0.0.1:5000/api/contacts/1/experiences/
```

**Delete one experience**

URL
```
http://<IP>:5000/api/contacts/<int:contact_id>/experiences/<int:experience_id>
```

Sample call:

```
curl -X DELETE http://127.0.0.1:5000/api/contacts/1/experiences/2
```


**Update one experience**

URL
```
http://<IP>:5000/api/contacts/<int:contact_id>/experiences/<int:experience_id>
```

Sample call:

```
curl -X PUT -d '{"type": "Work"}' http://127.0.0.1:5000/api/contacts/1/experiences/2
```

**View by experience type**

URL
```
http://<IP>:5000/api/contacts/<int:contact_id>/experiences/<string:type>
```

Sample call:

```
http://127.0.0.1:5000/api/contacts/1/experiences/Education
```

**Add experiences by list**

URL
```
http://<IP>:5000/api/contacts/<int:contact_id>/experiences/addByList
```

Sample Call:
```
curl --header "Content-Type: application/json" --request POST --data '[{			
          "description": "ok bye",
          "host": "Google",
          "title": "SDE",
          "date_start": "2010-02-09",
          "type": "Work",
          "degree":"Masters",
          "achievements": [{
        		"description":"hi",
        		"achievement_order":1
          }
          ]
}]' http://127.0.0.1:5000/api/contacts/1/experiences/

```

### Frontend

- Open a different terminal window
- Clone the branch wensi_resumeBuilder under baltimorecorps/webapp
- Go to webapp-master folder
` cd webapp-master`
- Start the frontend react app:
`npm start`
- The website page should automatically display on your default browser with the URL to be http://localhost:3000

On the homepage’s nav bar, click “TalentProfile”.
- Test add experience: click the plus icon on the right, fill the form, and click Submit
- Test edit experience: click the edit icon, fill out the form, and click Submit
- Test delete experience: click the delete icon

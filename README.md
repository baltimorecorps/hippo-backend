# Resume Builder API
[![Dev Build Status](https://travis-ci.com/baltimorecorps/hippo-backend.svg?branch=dev)](https://travis-ci.com/baltimorecorps/hippo-backend)
## Getting set up for development

### Dependencies for development
- Python 3.7 (or later)
- Postgres 11.x
  - Used for unit tests
- Docker
- Keybase

### Getting Started:
- Install the dependencies listed above
- Run `scripts/setup.sh`, which will automatically do the following
  - Set up a virtual env (in the `env` directory)
  - Set up a local database (running in docker)
  - Clone the secrets repository
- `source env/bin/activate` to enter the virtualenv
- `pytest` to ensure all unit tests run and pass
- `python run.py` to start the server

Quickstart version (can be copy/pasted into terminal)
```
python --version
psql --version
docker --version
keybase --version

scripts/setup.sh
source env/bin/activate
pytest
export TRELLO_API_KEY=<api key>
export TRELLO_API_TOKEN=<token>
python run.py
```
### Must set local environtment variables everytime before running the server
Trello keys are in the dev.cfg file in secrets/

## Database

### Working with the local database
As part of `scripts/setup.sh`, a new docker container is started running a
local database. This database will lose all data every time it is stopped and
be reinitialized every time it is restarted (using the current database
migrations)

The following scripts are provided for working with this database
* `scripts/start_localdb.sh`
* `scripts/stop_localdb.sh`
* `scripts/restart_localdb.sh`
* `scripts/connect_localdb.sh`

### Connecting to the shared development database
For debugging purposes, you may want to connect your local server to the shared
development database running in Heroku. You can accomplish this by setting the
environment variable `DEPLOY_ENV=dev`.

```
export DEPLOY_ENV=dev
python run.py
```

### Database Migrations
We use `flask-migrate` (which in turn, mostly uses `alembic`) for managing 
database migrations. If you are starting development on this project, it is
recommended that you take the time to familiarize yourself with these tools:

* https://alembic.sqlalchemy.org/en/latest/tutorial.html 
* https://flask-migrate.readthedocs.io/en/latest/ 

Mostly, you will probably want to autogenerate migrations. You can do this with
the following commands, which will autogenerate a migration, then open it for
editing and review.

```
python migrate.py db migrate
python migrate.py db edit
```

Note that at the moment, [alembic doesn't do a great job of handling PostgreSQL enums](https://github.com/sqlalchemy/alembic/issues/278),
so if you have made changes to the database which include enums, you'll likely
run into issues and have to make manual edits to the migration.

Once you're happy with your migration, you can test it on your local db by
running the upgrade and downgrade scripts (make sure to actually test the
downgrade!)

```
python migrate.py db upgrade
python migrate.py db downgrade 
```

Finally, once you are happy with your migration, don't forget to add the
migration script to your next commit!

```
git add migrations/versions/
```

## Viewing the API

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
curl --header "Content-Type: application/json" --request POST --data '{"description":"hello world hello world hello world hello world", "host": "abc", "title": "xyz", "date_start": "2000-01-01", "date_end":"2010-01-01", "type": "Service"}' http://127.0.0.1:5000/api/contacts/1/experiences/
```

**Delete one experience**

URL
```
http://<IP>:5000/api/experiences/<int:experience_id>
```

Sample call:

```
curl -X DELETE http://127.0.0.1:5000/api/experiences/2
```


**Update one experience**

URL
```
http://<IP>:5000/api/experiences/<int:experience_id>
```

Sample call:

```
curl -X PUT -d '{"type": "Work"}' http://127.0.0.1:5000/api/experiences/2
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

**View all tags**
URL
```
http://<IP>:5000/api/tags/
```

**View one tag**
URL
```
http://<IP>:5000/api/tags/<int:tag_id>
```
Sample Call:
```
curl --header "Content-Type: application/json" --request POST --data '{      
          "name": "blahhhh",
          "type": "Function"
          }' http://127.0.0.1:5000/api/tags/1/
```

```
curl --header "Content-Type: application/json" --request DELETE http://127.0.0.1:5000/api/tags/1/
```

```
curl --header "Content-Type: application/json" --request PUT --data '{      
          "name": "blahhhh",
          "type": "Function"
          }' http://127.0.0.1:5000/api/tags/1/
```

**Tags associated with a contact**

URL
```
http://<IP>:5000/api/contacts/1/tags/
```

URL
```
http://<IP>:5000/api/contacts/1/tags/?type=<string type>
```

```
<<<<<<< HEAD
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
||||||| merged common ancestors
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
=======
curl --header "Content-Type: application/json" --request POST --data '{"contact_id":1, "tag_id": 1, "tag_item_order":2}' http://127.0.0.1:5000/api/contacts/1/tags/
```

```
curl --header "Content-Type: application/json" --request PUT --data '{"contact_id":1, "tag_id": 1, "tag_item_order":2}' http://127.0.0.1:5000/api/contacts/1/tags/3/
```

**Add a new achievement**

URL
```
http://<IP>:5000/api/experiences/<int:experience_id>/achievements/
```

Sample Call:
```
curl --header "Content-Type: application/json" --request POST --data '{"exp_id":"1", "contact_id":"1", "description":"AutoCAD certification", "achievement_order":"3"}' http://127.0.0.1:5000/api/experiences/1/achievements
```

**Update an achievement**

URL
```
http://<IP>:5000/api/achievements/<int:achievement_id>
```

Sample Call:
```
curl -X PUT -d '{"description":"Completed 30 hours of training"}' http://127.0.0.1:5000/api/achievements/9
```

**Delete an achievement**

URL
```
http://<IP>:5000/api/achievements/<int:achievement_id>
```

Sample Call:
```
curl -X DELETE http://127.0.0.1:5000/api/achievements/8
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

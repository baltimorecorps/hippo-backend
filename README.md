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
pip install -r requirements.txt 
pytest
export TRELLO_API_KEY=<api key>
export TRELLO_API_TOKEN=<token>
python run.py
```
### Must set local environtment variables everytime before running the server
Trello keys can be found in the config variables on Heroku

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

## Using the API

### With the Frontend

- Open a different terminal window
- Follow the install instructions on [Hippo Frontend](https://github.com/baltimorecorps/hippo-frontend)
- Run the app locally and login

After logging in:
- Test add experience: click the plus icon on the right, fill the form, and click Submit
- Test edit experience: click the edit icon, fill out the form, and click Submit
- Test delete experience: click the delete icon

## File Structure

- `change-sets/` Stores the markdown files with descriptions of changes made to each staging and feature branch

- `migrations/` Stores the migration scripts that upgrade or downgrade the prod and dev database when changes are made

- `models/` Stores the files that both describe the structure of each table in the database and determine which fields are dumped/loaded through the API

- `resources/` Stores the code that is run when a specific endpoint is. Each endpoint URL corresponds to a class and each HTTP method corresponds to a class method

- `scripts/` Stores some bash scripts that automate the setup of the development environment when first cloning the repo

- `tests/` Stores the unit and integration tests for the API, as well as the data needed to run those tests

- `Procfile` Tells heroku what type of dyno to use when running this app

- `.travis.yml` Tells Travis CI how to run the tests when new code is pushed

- `auth.py` Manages the authorization framework for the API 

- `app.py` Initializes the API server with the appropriate context from the configuration 

- `api.py` Maps the resource classes to specific URLs 

- `defaultcfg.py`

- `migrate_dev.py` Runs the migration scripts for the dev database when deploying to staging

- `migrate_prod.py` Runs the migration scripts for the prod database when deploying to prod

- `requirements.txt` Lists the package requirements to run the code in this repo

- `run.py` Starts the server to host the API by calling `app.py`

- `runtime.txt` File necessary to run the code on Heroku

- `setup.cfg`

- `uwsgi.ini` 

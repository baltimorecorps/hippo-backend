import os

import pytest
from testing.postgresql import Postgresql

from run import create_app
from models.base_model import db
from .populate_db import populate

_init_sql_path = os.path.join(os.path.dirname(__file__),
                              '..', 'common', 'init.sql')
with open(_init_sql_path, 'rb') as f:
    _init_sql = f.read().decode('utf8')

_init_sql_path = os.path.join(os.path.dirname(__file__),
                              '..', 'common', 'populate_db.sql')
with open(_init_sql_path, 'rb') as f:
    _populate_sql = f.read().decode('utf8')

@pytest.fixture(scope='session')
def _app(request):
    app = create_app('test')
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    app.config['CONTACT_DELETE_TOKEN'] = 'testing_token'

    with Postgresql() as postgresql:
        app.config['SQLALCHEMY_DATABASE_URI'] = postgresql.url()

        with app.app_context():
            db.init_app(app)
            db.create_all()
            populate(db)
            yield app

@pytest.fixture(scope='session')
def _db(_app):
    """
    Fixture needed to make pytest-flask-sqlalchemy work

    The '_app' fixture here is included to ensure that setup done in that
    fixture runs first.
    """

    return db

@pytest.fixture
def app(_app, db_session):
    """
    Fixture to grant access to the app client

    We include the 'db_session' fixture here to ensure that all tests are
    patched appropriately, so that any database changes made with a single
    test are reverted
    """

    return _app

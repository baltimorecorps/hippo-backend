import os

import pytest
from testing.postgresql import Postgresql

from run import create_app
from models.base_model import db
from common.populate_db import populate

_init_sql_path = os.path.join(os.path.dirname(__file__),
                              '..', 'common', 'init.sql')
with open(_init_sql_path, 'rb') as f:
    _init_sql = f.read().decode('utf8')

_init_sql_path = os.path.join(os.path.dirname(__file__),
                              '..', 'common', 'populate_db.sql')
with open(_init_sql_path, 'rb') as f:
    _populate_sql = f.read().decode('utf8')

@pytest.fixture(scope='module')
def app():
    app = create_app("config")
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    with Postgresql() as postgresql:
        app.config['SQLALCHEMY_DATABASE_URI'] = postgresql.url()

        with app.app_context():
            db.init_app(app)
            db.engine.execute(_init_sql)
            #db.engine.execute(_populate_sql)
            populate(db)
            yield app

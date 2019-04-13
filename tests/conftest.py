import pytest
from run import create_app
from models.base_model import db


@pytest.fixture
def app():
    app = create_app("config")
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"

    with app.app_context():
        db.init_app(app)
        db.create_all()
        yield app
        db.drop_all()

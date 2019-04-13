import pytest
# import sys, os
# sys.path.insert(0, os.path.abspath(os.path.join('..', 'run.py')))
# print(sys.path)
from run import create_app
import flask
from models.base_model import db
from api import api_bp
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask import Blueprint
# from flask_restful import Api

@pytest.fixture
def app():
    app = create_app("config")
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://:@localhost/mydb"
    # db = SQLAlchemy()

    with app.app_context():
        db.init_app(app)

        # db.engine.execute("GRANT ALL ON SCHEMA public TO newuser;")
        # db.engine.execute("GRANT ALL ON SCHEMA public TO public;")
        db.create_all()
        yield app
        #db.session.remove()
        db.engine.execute("drop schema if exists public cascade")
        db.engine.execute("create schema public")
        db.drop_all()

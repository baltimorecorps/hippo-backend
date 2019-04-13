import pytest
# import sys, os
# sys.path.insert(0, os.path.abspath(os.path.join('..', 'run.py')))
# print(sys.path)
from run import create_app
from models.base_model import db
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask import Blueprint
# from flask_restful import Api

@pytest.fixture
def app():
    app = create_app("config")
    app.config['DEBUG'] = True
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://skflpscmrdpxig:b5d9f1887753ae2dedf55325f7253f053a46388c685fa288ff1d4469b15fabe1@ec2-23-21-128-35.compute-1.amazonaws.com:5432/d8i4u0mq57b2cv"
    # db = SQLAlchemy()

    with app.app_context():
        db.init_app(app)

        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

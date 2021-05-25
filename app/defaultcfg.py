import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:localdbpw@localhost:5433/localdb"
    AUTH0_API_AUDIENCE = 'http://localhost:5000'
    SESSION_SECRET_KEY = b'not a real key'

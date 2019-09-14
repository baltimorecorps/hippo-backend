import os
from flask import Flask
from api import api_bp

def load_from_dev(app):
    app.config.from_pyfile('secrets/dev.cfg')

def load_from_env(app):
    if os.environ.get('DATABASE_URL'):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

def load_config(app):
    if os.environ.get('DEPLOY_ENV') == 'dev':
        load_from_dev(app)
    else:
        load_from_env(app)

def create_app():
    app = Flask(__name__)
    app.config.from_object('defaultcfg')
    load_config(app)
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def home_page():
    	return 'Home page'

    from models.base_model import db
    db.init_app(app)
    return app

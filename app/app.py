import os
import os.path

from flask import Flask, jsonify, g, request
from flask_cors import CORS
from flask_login import LoginManager

from app.api import api_bp
from app.auth import AuthError
from app.models import UserSession
from app.defaultcfg import Config

def load_from_dev(app):
    if os.path.isfile('secrets/dev.cfg'):
        app.config.from_pyfile('secrets/dev.cfg')
    else:
        load_from_env(app)

def load_from_prod(app):
    if os.path.isfile('secrets/prod.cfg'):
        app.config.from_pyfile('secrets/prod.cfg')
    else:
        load_from_env(app)

def load_from_env(app):
    if os.environ.get('DATABASE_URL'):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    def load_var(name):
        if os.environ.get(name):
            app.config[name] = os.environ[name]

    load_var('AUTH0_API_AUDIENCE')
    load_var('TRELLO_API_KEY')
    load_var('TRELLO_API_TOKEN')
    load_var('SESSION_SECRET_KEY')
    load_var('CONTACT_DELETE_TOKEN')

def load_config(app, env):
    if env is None:
        env = os.environ.get('DEPLOY_ENV')

    if env == 'local':
        load_from_env(app)
    elif env == 'dev':
        load_from_dev(app)
    elif env == 'prod':
        load_from_prod(app)
    else:
        if env is None:
            env = 'default'
        load_from_env(app)

    if env == 'test':
        app.config['LOGIN_DISABLED'] = True

    app.config['DEPLOY_ENV'] = env

def create_app(env=None):
    app = Flask(__name__)


    # Initialize app config
    app.config.from_object(Config)
    load_config(app, env)

    # CORS setup
    CORS(app, supports_credentials=True)

    # Sessions related initialization
    app.secret_key = app.config['SESSION_SECRET_KEY']
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Initialization for flask-restful
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def home_page():
        return 'Hi'

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    @login_manager.user_loader
    def load_user(user_id):
        return UserSession.query.get(user_id)

    @login_manager.request_loader
    def load_test_user(user_id):
        if (app.config.get('TESTING')
                and request.headers.get('X-Test-Authz')):
            assert app.config.get('DEPLOY_ENV') == 'test'
            return g.test_user
        return None


    from app.models.base_model import db
    db.init_app(app)
    return app

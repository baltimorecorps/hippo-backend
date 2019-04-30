from flask import Flask
from api import api_bp


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def home_page():
    	return 'Home page'

    from models.base_model import db
    db.init_app(app)
    return app

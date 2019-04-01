from flask import Flask
from flask_restful import Resource, reqparse, Api
from resources.Contacts import ContactAll

application = Flask(__name__)
api = Api(application)
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://skflpscmrdpxig:b5d9f1887753ae2dedf55325f7253f053a46388c685fa288ff1d4469b15fabe1@ec2-23-21-128-35.compute-1.amazonaws.com:5432/d8i4u0mq57b2cv'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['PROPAGATE_EXCEPTIONS'] = True

from models.base_model import db
db.init_app(application)

from app import api_bp
application.register_blueprint(api_bp, url_prefix='/api')
    
api.add_resource(ContactAll, '/', '/contacts')
api.add_resource(ContactOne, '/contacts/<int:contact_id>', '/contacts')


if __name__=='__main__':
    application.run(debug=True)

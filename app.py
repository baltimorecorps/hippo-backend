from flask import Flask
from flask_restful import Resource, reqparse, Api
from resources.Contacts import ContactAll, ContactOne
from resources.Experience import ExperienceAll, ExperienceOne

application = Flask(__name__)
api = Api(application)
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://skflpscmrdpxig:b5d9f1887753ae2dedf55325f7253f053a46388c685fa288ff1d4469b15fabe1@ec2-23-21-128-35.compute-1.amazonaws.com:5432/d8i4u0mq57b2cv'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['PROPAGATE_EXCEPTIONS'] = True

from models.base_model import db
db.init_app(application)

api.add_resource(ContactAll, '/', '/contacts')
api.add_resource(ContactOne, '/contacts/<int:contact_id>', '/contacts')
api.add_resource(Profile, '/contacts/<int:contact_id>/profile')
api.add_resource(ExperienceAll, '/contacts/<int:contact_id>/experiences/')
api.add_resource(ExperienceOne, '/contacts/<int:contact_id>/experiences/',
                 '/contacts/<int:contact_id>/experiences/<int:experience_id>')

if __name__=='__main__':
    application.run(debug=True)

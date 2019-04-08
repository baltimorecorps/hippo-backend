from flask import Blueprint
from flask_restful import Api
from resources.Contacts import ContactAll, ContactOne, Profile
from resources.Tag import TagAll, TagOne, TagItemQuery
from resources.Experience import ExperienceAll, ExperienceOne, ExperienceList, ExperienceType

application = Flask(__name__)
api = Api(application)
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://skflpscmrdpxig:b5d9f1887753ae2dedf55325f7253f053a46388c685fa288ff1d4469b15fabe1@ec2-23-21-128-35.compute-1.amazonaws.com:5432/d8i4u0mq57b2cv'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['PROPAGATE_EXCEPTIONS'] = True

from models.base_model import db
db.init_app(application)

api.add_resource(ContactAll, '/contacts/', '/')
api.add_resource(ContactOne, '/contacts/<int:contact_id>', '/contacts/')
api.add_resource(Profile, '/contacts/<int:contact_id>/profile')
api.add_resource(ExperienceAll, '/contacts/<int:contact_id>/experiences/')
api.add_resource(ExperienceOne, '/contacts/<int:contact_id>/experiences/',
                 '/contacts/<int:contact_id>/experiences/<int:experience_id>')
api.add_resource(TagAll, '/tags')
api.add_resource(TagOne, '/tags/<int:tag_id>')
api.add_resource(TagItemQuery, '/contacts/<int:contact_id>/tags/','/contacts/<int:contact_id>/tags/<int:tagitem_id>')
api.add_resource(ExperienceType,'/contacts/<int:contact_id>/experiences/<string:type>')
api.add_resource(ExperienceList, '/contacts/<int:contact_id>/experiences/addByList')

if __name__=='__main__':
    application.run(debug=True)

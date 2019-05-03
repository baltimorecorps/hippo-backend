from flask import Blueprint
from flask_restful import Api
from resources.Contacts import ContactAll, ContactOne, Profile
from resources.Tag import TagAll, TagOne, TagItemQuery
from resources.Experience import ExperienceAll, ExperienceOne, ExperienceList
from resources.Achievement import AchievementsAll, AchievementOne
from resources.Resume import ContactsResume, ResumeOne, ResumeSections

api_bp = Blueprint('api',__name__)
api = Api(api_bp)

# Route
api.add_resource(ContactAll, '/contacts/', '/contacts', '/')
api.add_resource(ContactOne, '/contacts/<int:contact_id>', '/contacts/')
api.add_resource(Profile, '/contacts/<int:contact_id>/profile')
api.add_resource(ExperienceAll, '/contacts/<int:contact_id>/experiences/', '/contacts/<int:contact_id>/experiences')
api.add_resource(ExperienceOne, '/experiences/<int:experience_id>', '/experiences/<int:experience_id>/')
api.add_resource(ExperienceList, '/contacts/<int:contact_id>/experiences/addByList', '/contacts/<int:contact_id>/experiences/addByList/')
api.add_resource(TagAll, '/tags/', '/tags')
api.add_resource(TagOne, '/tags/<int:tag_id>', '/tags/<int:tag_id>/')
api.add_resource(TagItemQuery, '/contacts/<int:contact_id>/tags/','/contacts/<int:contact_id>/tags',
	'/contacts/<int:contact_id>/tags/<int:tagitem_id>','/contacts/<int:contact_id>/tags/<int:tagitem_id>/')
api.add_resource(AchievementsAll, '/experiences/<int:experience_id>/achievements')
api.add_resource(AchievementOne, '/achievements/<int:achievement_id>')
api.add_resource(ContactsResume, '/contacts/<int:contact_id>/resumes/','/contacts/<int:contact_id>/resumes')
api.add_resource(ResumeOne, '/resumes/<int:resume_id>/','/resumes/<int:resume_id>')
api.add_resource(ResumeSections, '/resumes/<int:resume_id>/sections/','/resumes/<int:resume_id>/sections')

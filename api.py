from flask import Blueprint
from flask_restful import Api
from resources.Contacts import ContactAll, ContactOne
from resources.Tag import TagAll, TagOne, TagItemAll, TagItemOne
from resources.Experience import ExperienceAll, ExperienceOne
from resources.Achievement import AchievementAll
from resources.Resume import ResumeAll, ResumeOne, GenerateResume
from resources.Resume import ResumeSectionAll, ResumeSectionOne

api_bp = Blueprint('api',__name__)
api = Api(api_bp)

# Route
api.add_resource(ContactAll,
                 '/contacts/',
                 '/contacts',
                 '/')
api.add_resource(ContactOne,
                 '/contacts/<int:contact_id>',
                 '/contacts/<int:contact_id>/')
api.add_resource(ExperienceAll,
                '/contacts/<int:contact_id>/experiences/',
                '/contacts/<int:contact_id>/experiences')
api.add_resource(ExperienceOne,
                 '/experiences/<int:experience_id>',
                 '/experiences/<int:experience_id>/')
api.add_resource(TagAll,
                 '/tags/',
                 '/tags')
api.add_resource(TagOne,
                 '/tags/<int:tag_id>',
                 '/tags/<int:tag_id>/')
api.add_resource(TagItemAll,
                 '/contacts/<int:contact_id>/tags/',
                 '/contacts/<int:contact_id>/tags')
api.add_resource(TagItemOne,
                 '/contacts/<int:contact_id>/tags/<int:tag_id>',
                 '/contacts/<int:contact_id>/tags/<int:tag_id>/')
api.add_resource(AchievementAll,
                 '/contacts/<int:contact_id>/achievements/',
                 '/contacts/<int:contact_id>/achievements')
api.add_resource(ResumeAll,
                 '/contacts/<int:contact_id>/resumes/',
                 '/contacts/<int:contact_id>/resumes')
api.add_resource(ResumeOne,
                 '/resumes/<int:resume_id>/',
                 '/resumes/<int:resume_id>')
api.add_resource(ResumeSectionAll,
                 '/resumes/<int:resume_id>/sections/',
                 '/resumes/<int:resume_id>/sections')
api.add_resource(ResumeSectionOne,
                 '/resumes/<int:resume_id>/sections/<int:section_id>',
                 '/resumes/<int:resume_id>/sections/<int:section_id>/')
api.add_resource(GenerateResume,
                 '/contacts/<int:contact_id>/generate-resume/')

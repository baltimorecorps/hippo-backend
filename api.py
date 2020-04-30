from flask import Blueprint
from flask_restful import Api
from resources.Contacts import ContactAll, ContactOne, ContactAccount, ContactShort
from resources.Tag import TagAll, TagOne, TagItemAll, TagItemOne
from resources.Experience import ExperienceAll, ExperienceOne
from resources.Achievement import AchievementAll
from resources.Resume import ResumeAll, ResumeOne, GenerateResume
from resources.Resume import ResumeSectionAll, ResumeSectionOne
from resources.Skills import ContactSkills, ContactSkillOne, AutocompleteSkill
from resources.Capability import (
    CapabilityRecommended,
    ContactCapabilities,
    ContactCapabilitySuggestions,
    ContactCapabilitySuggestionOne,
)
from resources.Session import Session
from resources.ProgramContacts import (
    ProgramContactOne,
    ProgramContactAll,
    ProgramContactApproveMany,
    ApplicationsInternal
)
from resources.Trello_Intake_Talent import (
    IntakeTalentBoard,
    IntakeTalentCard,
    ReviewTalentCard
)
from resources.Opportunity import (
    OpportunityAll,
    OpportunityAllInternal,
    OpportunityOne,
    OpportunityOneOrg,
    OpportunityDeactivate,
    OpportunityActivate,
)
from resources.OpportunityApp import (
    OpportunityAppReject,
    OpportunityAppAll,
    OpportunityAppOne,
    OpportunityAppSubmit,
    OpportunityAppRecommend,
    OpportunityAppReopen,
    OpportunityAppInterview,
    OpportunityAppConsider,
)
from resources.FormAssembly import (
    TalentProgramApp,
    OpportunityIntakeApp,
)

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(ContactAll,
                 '/contacts/',
                 '/contacts',
                 '/')
api.add_resource(ContactOne,
                 '/contacts/<int:contact_id>',
                 '/contacts/<int:contact_id>/')
api.add_resource(ContactAccount,
                 '/contacts/me',
                 '/contacts/me/')
api.add_resource(ContactShort,
                 '/contacts/short',
                 '/contacts/short/')
api.add_resource(ContactSkills,
                 '/contacts/<int:contact_id>/skills',
                 '/contacts/<int:contact_id>/skills/')
api.add_resource(ContactSkillOne,
                 '/contacts/<int:contact_id>/skills/<string:skill_id>',
                 '/contacts/<int:contact_id>/skills/<string:skill_id>/')
api.add_resource(ContactCapabilities,
                 '/contacts/<int:contact_id>/capabilities/',
                 '/contacts/<int:contact_id>/capabilities/')
api.add_resource(ContactCapabilitySuggestions,
                 '/contacts/<int:contact_id>/capabilities/<string:capability_id>/suggestion',
                 '/contacts/<int:contact_id>/capabilities/<string:capability_id>/suggestion/')
api.add_resource(ContactCapabilitySuggestionOne,
                 '/contacts/<int:contact_id>/capabilities/<string:capability_id>/suggestion/<string:skill_id>',
                 '/contacts/<int:contact_id>/capabilities/<string:capability_id>/suggestion/<string:skill_id>/')
api.add_resource(CapabilityRecommended,
                 '/capabilities',
                 '/capabilities/')
api.add_resource(AutocompleteSkill,
                 '/skills/autocomplete',
                 '/skills/autocomplete/')
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
api.add_resource(ProgramContactAll,
                 '/contacts/<int:contact_id>/programs',
                 '/contacts/<int:contact_id>/programs/')
api.add_resource(ProgramContactOne,
                 '/contacts/<int:contact_id>/programs/<int:program_id>',
                 '/contacts/<int:contact_id>/programs/<int:program_id>/')
api.add_resource(ProgramContactApproveMany,
                 '/programs/<int:program_id>/contacts/approve-many',
                 '/programs/<int:program_id>/contacts/approve-many/')
api.add_resource(ApplicationsInternal,
                 '/internal/applications',
                 '/internal/applications/')
api.add_resource(OpportunityAppOne,
                 '/contacts/<int:contact_id>/app/<string:opportunity_id>',
                 '/contacts/<int:contact_id>/app/<string:opportunity_id>/')
api.add_resource(OpportunityAppSubmit,
                 '/contacts/<int:contact_id>/app/<string:opportunity_id>/submit',
                 '/contacts/<int:contact_id>/app/<string:opportunity_id>/submit/')
api.add_resource(OpportunityAppReject,
                 '/contacts/<int:contact_id>/app/<string:opportunity_id>/not-a-fit',
                 '/contacts/<int:contact_id>/app/<string:opportunity_id>/not-a-fit/')
api.add_resource(OpportunityAppInterview,
                 '/contacts/<int:contact_id>/app/<string:opportunity_id>/interview',
                 '/contacts/<int:contact_id>/app/<string:opportunity_id>/interview/')
api.add_resource(OpportunityAppConsider,
                 '/contacts/<int:contact_id>/app/<string:opportunity_id>/consider',
                 '/contacts/<int:contact_id>/app/<string:opportunity_id>/consider/')
api.add_resource(OpportunityAppAll,
                 '/contacts/<int:contact_id>/app',
                 '/contacts/<int:contact_id>/app/')
api.add_resource(OpportunityAppRecommend,
                 '/contacts/<int:contact_id>/app/<string:opportunity_id>/recommend',
                 '/contacts/<int:contact_id>/app/<string:opportunity_id>/recommend/')
api.add_resource(OpportunityAppReopen,
                 '/contacts/<int:contact_id>/app/<string:opportunity_id>/reopen',
                 '/contacts/<int:contact_id>/app/<string:opportunity_id>/reopen/')
api.add_resource(IntakeTalentBoard,
                 '/programs/<int:program_id>/trello/intake-talent',
                 '/programs/<int:program_id>/trello/intake-talent/')
api.add_resource(IntakeTalentCard,
                 '/contacts/<int:contact_id>/programs/<int:program_id>/trello/intake-talent',
                 '/contacts/<int:contact_id>/programs/<int:program_id>/trello/intake-talent/')
api.add_resource(ReviewTalentCard,
                 '/reviews/<int:review_id>/trello/review-talent',
                 '/reviews/<int:review_id>/trello/review-talent/')
api.add_resource(TalentProgramApp,
                 '/form-assembly/talent-app',
                 '/form-assembly/talent-app/')
api.add_resource(OpportunityIntakeApp,
                 '/form-assembly/opportunity-app',
                 '/form-assembly/opportunity-app/')
api.add_resource(Session,
                 '/session/',
                 '/session')
api.add_resource(OpportunityAll,
                 '/opportunity',
                 '/opportunity/')
api.add_resource(OpportunityAllInternal,
                 '/internal/opportunities/',
                 '/internal/opportunities')
api.add_resource(OpportunityOne,
                 '/opportunity/<string:opportunity_id>',
                 '/opportunity/<string:opportunity_id>/')
api.add_resource(OpportunityOneOrg,
                 '/org/opportunities/<string:opportunity_id>',
                 '/org/opportunities/<string:opportunity_id>/')
api.add_resource(OpportunityDeactivate,
                 '/opportunity/<string:opportunity_id>/deactivate',
                 '/opportunity/<string:opportunity_id>/deactivate/')
api.add_resource(OpportunityActivate,
                 '/opportunity/<string:opportunity_id>/activate',
                 '/opportunity/<string:opportunity_id>/activate/')

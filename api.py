from flask import Blueprint
from flask_restful import Api
from resources.Contacts import (
    ContactAll,
    ContactOne,
    ContactAccount,
    ContactShort,
    ContactFull,
    ContactApproveMany
)
from resources.Experience import ExperienceAll, ExperienceOne
from resources.Skills import ContactSkills, ContactSkillOne, AutocompleteSkill
from resources.Capability import (
    CapabilityRecommended,
    ContactCapabilities,
    ContactCapabilitySuggestions,
    ContactCapabilitySuggestionOne,
)
from resources.Session import Session
from resources.ProgramApp import (
    ContactProgramAppsOne,
    ContactProgramAppsAll,
    ContactProgramAppsInterested
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
from resources.Profile import ProfileOne, ContactInstructions, ProfileSubmit
from resources.Program import ProgramAll
from resources.Filter import Filter

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
                 '/contacts/short/',
                 '/contacts',
                 '/contacts/')
api.add_resource(ContactApproveMany,
                 '/contacts/approve',
                 '/contacts/approve/')
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
api.add_resource(ProfileOne,
                 '/contacts/<int:contact_id>/about-me',
                 '/contacts/<int:contact_id>/about-me/')
api.add_resource(ContactProgramAppsOne,
                 '/contacts/<int:contact_id>/program-apps',
                 '/contacts/<int:contact_id>/program-apps/')
api.add_resource(ContactProgramAppsAll,
                 '/contacts/program-apps',
                 '/contacts/program-apps/')
api.add_resource(ContactProgramAppsInterested,
                 '/contacts/<int:contact_id>/program-apps/interested',
                 '/contacts/<int:contact_id>/program-apps/interested/')
api.add_resource(ContactInstructions,
                 '/contacts/<int:contact_id>/instructions',
                 '/contacts/<int:contact_id>/instructions/')
api.add_resource(ProfileSubmit,
                 '/contacts/<int:contact_id>/submit',
                 '/contacts/<int:contact_id>/submit/',
                 '/contacts/<int:contact_id>/profile/submit',
                 '/contacts/<int:contact_id>/profile/submit/')
api.add_resource(ProgramAll,
                 '/programs',
                 '/programs/')
api.add_resource(ContactFull,
                 '/contacts/<int:contact_id>/profile',
                 '/contacts/<int:contact_id>/profile/')
api.add_resource(Filter,
                 '/contacts/filter',
                 '/contacts/filter/')

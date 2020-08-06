from flask_restful import Resource, request
from flask_login import login_required

from models.base_model import db
from models.contact_model import Contact, ContactSchema
from models.profile_model import (
    Profile,
    Race,
    ContactAddress,
    RoleChoice,
    ProgramsCompleted
)
from .Trello_Intake_Talent import get_intake_talent_board_id
from .trello_utils import (
    query_board_data,
    update_card,
    Board,
    Card,
    BoardList
)

from marshmallow import ValidationError

from auth import (
    refresh_session,
    is_authorized_view,
    is_authorized_write,
    unauthorized
)


profile_schema = ContactSchema(exclude=['skills',
                                        'programs',
                                        'program_apps',
                                        'terms_agreement',
                                        'account_id',
                                        'email_primary',
                                        'instructions'])
instructions_schema = ContactSchema(exclude=['skills',
                                             'programs',
                                             'program_apps',
                                             'phone_primary',
                                             'terms_agreement',
                                             'account_id',
                                             'email_primary',
                                             'profile'])

def create_profile(contact):
    profile = Profile(contact=contact)
    profile.addresses.append(ContactAddress(contact=contact))
    profile.race = Race(contact=contact)
    profile.roles = RoleChoice()
    profile.programs_completed = ProgramsCompleted()
    return profile

class ProfileOne(Resource):
    method_decorators = {
        'get': [login_required, refresh_session],
        'put': [login_required, refresh_session],
        'post': [login_required, refresh_session],
    }


    def get(self, contact_id):
        if not is_authorized_view(contact_id):
            return unauthorized()

        contact = Contact.query.get(contact_id)
        if not contact.profile:
            return {'message': 'Profile does not exist'}, 404

        result = profile_schema.dump(contact)
        return {'status': 'success', 'data': result}, 200

    def post(self, contact_id):
        if not is_authorized_view(contact_id):
            return unauthorized()

        contact = Contact.query.get(contact_id)

        if not contact:
            return {'message': 'Contact does not exist'}, 404

        if contact.profile:
            return {'message': 'Profile already exists'}, 400

        profile = create_profile(contact)
        db.session.add(profile)
        db.session.commit()

        result = profile_schema.dump(contact)

        return {'status': 'success', 'data': result}, 201

    def put(self, contact_id):
        if not is_authorized_write(contact_id):
            return unauthorized()

        json_data = request.get_json(force=True)

        contact = Contact.query.get(contact_id)
        if not contact:
            return {'message': 'Contact does not exist'}, 404

        try:
            data = profile_schema.load(json_data)
        except ValidationError as e:
            return e.messages, 422

        profile_data = data.pop('profile', None)
        contact.update(**data)
        contact.profile.update(**profile_data)
        email = data.get('email', None)
        if email:
            contact.email_primary.email = email
        db.session.commit()

        result = profile_schema.dump(contact)

        return {'status': 'success', 'data': result}, 200

class ContactInstructions(Resource):

    method_decorators = {
        'get': [login_required, refresh_session],
    }

    def get(self, contact_id):
        if not is_authorized_view(contact_id):
            return unauthorized()
        contact = Contact.query.get(contact_id)
        if not contact:
            return {'message': 'Contact does not exist'}, 404
        result = instructions_schema.dump(contact)
        return {'status': 'success', 'data': result}, 200


class ProfileSubmit(Resource):

    method_decorators = {
        'post': [login_required, refresh_session],
    }

    def post(self, contact_id):
        if not is_authorized_view(contact_id):
            return unauthorized()

        # query contact and check that all submission criteria is met
        contact = Contact.query.get(contact_id)
        if not contact:
            return {'message': 'Contact does not exist'}, 404
        if not (contact.about_me_complete['is_complete']
                and contact.profile_complete['is_complete']):
            return {'message': 'Not all profile sections are complete'}, 400
        if contact.stage >= 2:
            return {'message': 'Profile already submitted'}, 400

        # Start of Trello specific code
        PROGRAMS_DICT = {
            'Fellowship': 'Fellowship',
            'Mayoral Fellowship': 'Mayoral Fellowship',
            'Place for Purpose': 'PFP',
            'Public Allies': 'PA',
            'JHU Carey Humanities Fellowship': 'JHU - Carey'
        }

        # get board_id and card_id
        board_id = get_intake_talent_board_id(program_id=1)
        if not contact.card_id:
            card_id = contact.programs[0].card_id
            contact.card_id = card_id
        else:
            card_id = contact.card_id

        #query board and card
        board = Board(query_board_data(board_id))
        card = board.cards.get(card_id)
        profile = contact.profile

        # check that the card exists and that it's not already in stage 2
        if not card:
            return {'message': 'No intake card found'}, 400
        elif card.stage >= 2:
            return {'message': 'Application has already been submitted'}, 400

        # parses form data to fill the card description
        roles = ['- '+role for role in profile.roles_list]
        roles_str = '\n'.join(roles)
        programs = [PROGRAMS_DICT[app.program.name]
                    for app in contact.program_apps
                    if app.is_interested]
        programs_str = '\n'.join(['- ' + p for p in programs])
        new_labels = set(card.label_names + programs)

        #formats the string for the description
        card_data = {
            'name': (
                f"{contact.first_name} {contact.last_name}"
                ),
            'desc': (
                "**Racial Equity & Baltimore: "
                "Why is racial equity work in Baltimore "
                "important to you?**\n\n"
                f"{profile.value_question1}\n\n---\n\n"
                "**Sector Effectiveness: How has your background"
                " and experiences prepared you for today’s work"
                " in Baltimore’s social impact sector?**\n\n"
                f"{profile.value_question2}\n\n---\n\n"
                f"**Level of Experience:** {profile.years_exp}\n\n"
                f"**Types of roles they're interested in:**\n\n"
                f"{roles_str}\n\n---\n\n"
                f"**Programs/Services they are interested in:**\n\n"
                f"{programs_str}\n\n---\n\n"
            )
        }

        #updates the card with the information parsed from the form
        card.update(**card_data)
        card.add_attachment(
            url=f'https://app.baltimorecorps.org/profile/{contact_id}',
            name='Profile'
        )
        card.set_labels(new_labels)

        # moves card to submitted list
        submitted_list = board.lists['stage'][2]
        card.move_card(submitted_list)

        # updates the contact to stage 2
        contact.stage = 2
        db.session.commit()

        result = instructions_schema.dump(contact)

        return {'status': 'success', 'data': result}, 201

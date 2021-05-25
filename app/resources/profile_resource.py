from flask_restful import Resource, request
from flask_login import login_required
from marshmallow import ValidationError

from app.schemas import ContactSchema
from app.models import (
    db,
    Program,
    Contact,
    Profile,
    Race,
    ContactAddress,
    RoleChoice,
    ProgramsCompleted,
)
from app.resources.trello_utils import (
    query_board_data,
    update_card,
    Board,
    Card,
    BoardList
)
from app.auth import (
    refresh_session,
    is_authorized_view,
    is_authorized_write,
    unauthorized
)


profile_schema = ContactSchema(exclude=['skills',
                                        'program_apps',
                                        'email_primary',
                                        'instructions',
                                        'experiences'])
instructions_schema = ContactSchema(exclude=['skills',
                                             'program_apps',
                                             'email_primary',
                                             'profile',
                                             'experiences'])

def create_profile(contact):
    profile = Profile(contact=contact)
    profile.addresses.append(ContactAddress(contact=contact))
    profile.race = Race(contact=contact)
    profile.roles = RoleChoice()
    profile.programs_completed = ProgramsCompleted()
    return profile

def get_intake_talent_board_id(program_id):
    program = Program.query.get(program_id)
    return program.trello_board_id

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
        email = contact.email_main
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

        #query board and check that a card doesn't already exist
        board_id = get_intake_talent_board_id(program_id=1)
        board = Board(query_board_data(board_id))
        existing_card = board.find_card_by_custom_field('Email', email)
        if existing_card:
            return {'message': 'Application has already been submitted'}, 400

        # parses form data to fill the card description
        profile = contact.profile
        roles = ['- '+role for role in profile.roles_list]
        roles_str = '\n'.join(roles)
        programs = [PROGRAMS_DICT[app.program.name]
                    for app in contact.program_apps
                    if app.is_interested]
        programs_str = '\n'.join(['- ' + p for p in programs])

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
                f"**Currently a student:**\n\n"
                f"{profile.current_edu_status}\n\n---\n\n"
            )
        }
        fields_data = {
            'Phone': contact.phone_primary,
            'Email': email,
            'External ID': str(contact.id)
        }

        #creates the card with the information parsed from the form
        submitted_list = board.lists['stage'][2]
        card = submitted_list.add_card_from_template(**card_data)
        card.add_attachment(
            url=f'https://app.baltimorecorps.org/profile/{contact_id}',
            name='Profile'
        )
        labels = set(card.label_names + programs)
        card.set_labels(labels)
        card.set_custom_field_values(**fields_data)

        # updates the contact to stage 2
        contact.stage = 2
        contact.card_id = card.id
        db.session.commit()

        result = instructions_schema.dump(contact)

        return {'status': 'success', 'data': result}, 201

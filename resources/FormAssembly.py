from flask_restful import Resource, request
from models.base_model import db
from models.contact_model import Contact
from models.program_contact_model import ProgramContact, ProgramContactSchema
from models.opportunity_model import OpportunitySchema, OpportunityStage
from models.program_model import Program
from .Trello_Intake_Talent import get_intake_talent_board_id
from .ProgramContacts import query_one_program_contact
from .Opportunity import create_new_opportunity
from .trello_utils import (
    query_board_data,
    update_card,
    Board,
    Card,
    BoardList
)

opportunity_schema = OpportunitySchema()
program_contact_schema = ProgramContactSchema()


class TalentProgramApp(Resource):

    def post(self):
        form_data = request.form
        contact_id = int(form_data.get('contact_id'))
        program_id = int(form_data.get('program_id'))
        if not (contact_id or program_id):
            return {'message': 'No contact_id or program_id provided'}, 400
        program_contact = query_one_program_contact(contact_id, program_id)
        contact = Contact.query.get(contact_id)
        if not program_contact:
            return {'message': 'No program_contact record found'}, 400

        board_id = get_intake_talent_board_id(program_id)
        board = Board(query_board_data(board_id))
        email = contact.email_main
        existing_card = board.find_card_by_custom_field('Email', email)
        if existing_card:
            print(existing_card.name)
            print(existing_card.id)
            return {'message': 'Application has already been submitted'}, 400

        # parses form data to fill the card description
        capabilities = ['- '+v for k,v in form_data.items()
                        if 'capabilities' in k]
        capabilities_str = '\n'.join(capabilities)
        programs = [v for k,v in form_data.items() if 'programs' in k]
        programs_str = '\n'.join(['- ' + p for p in programs ])
        if form_data.get('mayoral_eligible'):
            mayoral_eligible = form_data.get('mayoral_eligible')
        else:
            mayoral_eligible = "N/A"
        if form_data.get('carey_eligible'):
            carey_eligible = form_data.get('carey_eligible')
        else:
            carey_eligible = "N/A"

        #formats the string for the description
        card_data = {
            'name': (
                f"{form_data.get('first_name')} {form_data.get('last_name')}"
                ),
            'desc': (
                "**Racial Equity & Baltimore: "
                "Why is racial equity work in Baltimore "
                "important to you?**\n\n"
                f"{form_data['equity']}\n\n---\n\n"
                "**Sector Effectiveness: How has your background"
                " and experiences prepared you for today’s work"
                " in Baltimore’s social impact sector?**\n\n"
                f"{form_data['effectiveness']}\n\n---\n\n"
                f"**Level of Experience:** {form_data['experience']}\n\n"
                f"**Types of roles they're interested in:**\n\n"
                f"{capabilities_str}\n\n---\n\n"
                f"**Programs/Services they are interested in:**\n\n"
                f"{programs_str}\n\n---\n\n"
                f"**Eligibility:**\n\n"
                f"- **Mayoral Fellowship:** {mayoral_eligible}\n"
                f"- **JHU - Carey:** {carey_eligible}\n"
            )
        }

        fields_data = {
            'Phone': contact.phone_primary,
            'Email': email,
            'External ID': str(contact.id)
        }

        #updates the card with the information parsed from the form
        submitted_list = board.lists['stage'][2]
        card = submitted_list.add_card_from_template(**card_data)
        card.add_attachment(
            url=f'https://app.baltimorecorps.org/profile/{contact_id}',
            name='Profile'
        )
        card.add_attachment(
            url=f"https://app.formassembly.com/responses/view/{form_data['response_id']}",
            name='Full Response'
        )
        labels = set(card.label_names + programs)
        card.set_labels(labels)
        print(fields_data)
        result = card.set_custom_field_values(**fields_data)
        print(result)

        # updates program_contact and contact to stage 2
        program_contact.update(**{'stage': 2})
        contact.stage = 2
        contact.card_id = card.id
        db.session.commit()

        result = program_contact_schema.dump(program_contact)

        return {'status': 'success', 'data': result}, 201

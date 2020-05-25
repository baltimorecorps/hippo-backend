from flask_restful import Resource, request
from models.base_model import db
from models.program_contact_model import ProgramContact, ProgramContactSchema
from models.opportunity_model import OpportunitySchema, OpportunityStage
from models.program_model import Program
from models.review_model import Review
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

def get_matching_opp_board_id(program_id):
    program = Program.query.get(program_id)
    return program.current_cycle.match_opp_board_id

def get_review_talent_board_id(program_id):
    program = Program.query.get(program_id)
    return program.current_cycle.review_talent_board_id

def get_current_cycle_id(program_id):
    program = Program.query.get(program_id)
    return program.current_cycle.id

def find_opp_card(form_data):
    board_id = get_matching_opp_board_id(form_data['program_id'])
    board_data = query_board_data(board_id)
    board = Board(board_data)
    submitted_list = board.lists['stage'][1]
    gdoc_id = form_data['google_doc_id']
    opp_card = board.find_card_by_custom_field('Google Doc ID', gdoc_id)
    return opp_card, board

class OpportunityIntakeApp(Resource):
    def post(self):
        form_data = request.form
        opp_card, board = find_opp_card(form_data)
        if opp_card is None:
            return {'message': 'No card found'}, 404
        gdoc_id = form_data['google_doc_id']
        gdoc_link = f'https://docs.google.com/document/d/{gdoc_id}/edit'
        opp_data = {
            'title': form_data['title'],
            'short_description': '',
            'gdoc_id': gdoc_id,
            'card_id': opp_card.id,
            'stage': OpportunityStage.submitted.value,
            'gdoc_link': gdoc_link,
            'org_name': form_data['org'],
            'cycle_id': get_current_cycle_id(form_data['program_id'])
        }
        opp = create_new_opportunity(opp_data)
        opp_card.set_custom_field_values(**{'Opp ID': opp.id})
        # TODO: Figure out how to handle error values
        started_list = board.lists['stage'][0]
        submitted_list = board.lists['stage'][1]
        opp_card.checked_move_card(started_list, submitted_list)
        result = opportunity_schema.dump(opp)
        return {"status": 'success', 'data': result}, 201


class TalentProgramApp(Resource):

    def post(self):
        form_data = request.form
        contact_id = int(form_data.get('contact_id'))
        program_id = int(form_data.get('program_id'))
        if not (contact_id or program_id):
            return {'message': 'No contact_id or program_id provided'}, 400
        program_contact = query_one_program_contact(contact_id, program_id)
        if not program_contact:
            return {'message': 'No program_contact record found'}, 400

        board_id = get_intake_talent_board_id(program_id)
        card_id = program_contact.card_id
        board = Board(query_board_data(board_id))
        card = board.cards.get(card_id)
        if not card:
            return {'message': 'No intake card found'}, 400
        elif card.stage >= 2:
            return {'message': 'Application has already been submitted'}, 400

        # parses form data to fill the card description
        capabilities = ['- '+v for k,v in form_data.items()
                        if 'capabilities' in k]
        capabilities_str = '\n'.join(capabilities)
        programs = [v for k,v in form_data.items() if 'programs' in k]
        programs_str = '\n'.join(['- ' + p for p in programs ])
        new_labels = set(card.label_names + programs)
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

        #updates the card with the information parsed from the form
        card.update(**card_data)
        card.add_attachment(
            url=f'https://app.baltimorecorps.org/profile/{contact_id}',
            name='Profile'
        )
        card.add_attachment(
            url=f"https://app.formassembly.com/responses/view/{form_data['response_id']}",
            name='Full Response'
        )
        card.set_labels(new_labels)

        # moves card and updates program_contact to stage 2
        program_contact.update(**{'stage': 2})
        submitted_list = board.lists['stage'][2]
        card.move_card(submitted_list)
        result = program_contact_schema.dump(program_contact)
        print(form_data.get('programs'))
        return {'status': 'success', 'data': result}, 201

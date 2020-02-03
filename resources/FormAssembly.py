from flask_restful import Resource, request
from models.base_model import db
from models.program_contact_model import ProgramContact, ProgramContactSchema
from models.program_model import Program
from models.review_model import Review
from .Trello_Intake_Talent import get_intake_talent_board_id
from .ProgramContacts import query_one_program_contact
from .trello_utils import (
    query_board_data,
    Board,
    Card,
    BoardList
)

program_contact_schema = ProgramContactSchema()

def get_review_talent_board_id(program_id):
    program = Program.query.get(program_id)
    return program.current_cycle.review_talent_board_id

class TalentProgramApp(Resource):

    def post(self):
        form_data = request.form
        contact_id = int(form_data['contact_id'])
        program_id = int(form_data['program_id'])
        if not (contact_id or program_id):
            return {'message': 'No contact_id or program_id provided'}, 400
        program_contact = query_one_program_contact(contact_id, program_id)
        if not program_contact:
            return {'message': 'No program_contact record found'}, 400

        intake_board_id = get_intake_talent_board_id(program_id)
        review_board_id = get_review_talent_board_id(program_id)
        intake_card_id = program_contact.card_id
        intake_board_data = query_board_data(intake_board_id)
        review_board_data = query_board_data(review_board_id)

        intake_board = Board(intake_board_data)
        review_board = Board(review_board_data)
        intake_card = intake_board.cards.get(intake_card_id)
        if not intake_card:
            return {'message': 'No intake card found'}, 400
        submitted_list = intake_board.lists['stage'][2]
        to_review_list = review_board.lists['stage'][1]
        review_card_data = {
            'name': f'Applicant {contact_id}',
            'desc': (
                '**Racial Equity & Baltimore: '
                'Why is racial equity work in Baltimore '
                'important to you?**\n\n'
                f"{form_data['equity']}\n\n---\n\n"
                '**Sector Effectiveness: How has your background'
                ' and experiences prepared you for today’s work'
                ' in Baltimore’s social impact sector?**\n\n'
                f"{form_data['effectiveness']}\n\n"
            )
        }
        review_card = to_review_list.add_card_from_template(**review_card_data)
        if not review_card:
            return {'message': 'Issue creating review card'}, 400
        review = Review(card_id=review_card.id, stage=1)
        program_contact.reviews.append(review)
        program_contact.update(**{'stage': 2})
        intake_card.move_card(submitted_list)
        result = program_contact_schema.dump(program_contact)
        return {'status': 'success', 'data': result}, 201

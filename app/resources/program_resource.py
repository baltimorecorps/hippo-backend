from flask_restful import Resource, request

from app.models import Program
from app.schemas import ProgramSchema

program_schema = ProgramSchema(many=True)

class ProgramAll(Resource):
    def get(self):
        programs = Program.query.all()
        result = program_schema.dump(programs)
        return {'status': 'success', 'data': result}, 200

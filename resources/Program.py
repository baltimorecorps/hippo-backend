from flask_restful import Resource, request
from models.program_model import Program, ProgramSchema

program_schema = ProgramSchema(many=True)

class ProgramAll(Resource):
    def get(self):
        programs = Program.query.all()
        result = program_schema.dump(programs)
        return {'status': 'success', 'data': result}, 200

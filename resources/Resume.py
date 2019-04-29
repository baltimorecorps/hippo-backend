from flask_restful import Resource, request
from models.resume_model import Resume, ResumeSchema

resumes_schema = ResumeSchema(many=True)
resume_schema = ResumeSchema()


class ContactsResume(Resource):

    def get(self, contact_id):  
        res = Resume.query.filter_by(contact_id=contact_id)
        res_list = resumes_schema.dump(res).data

        return {'status': 'success', 'data': res_list}, 200

    def post(self, contact_id):
        json_data = request.get_json(force=True)

        if not json_data:
            return {'message': 'No input data provided'}, 400

        # Validate and deserialize input
        data, errors = resume_schema.load(json_data)
        if errors:
            return errors, 422

        res = Resume(**data)

        db.session.add(res)
        db.session.commit()
        result = resume_schema.dump(res).data

        return {"status": 'success', 'data': result}, 201

class ResumeOne(Resource):

    def get(self, resume_id):
        pass

    def delete(self, resume_id):
        pass

    def put(self, resume_id):
        pass


class ResumeSections(Resource):
    def get(self, resume_id):
        pass


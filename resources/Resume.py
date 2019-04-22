from flask_restful import Resource, request
from models.resume_model import Resume, ResumeSchema
from models.base_model import db

resume_schema = ResumeSchema()
resumes_schema = ResumeSchema(many=True)


class ContactsResume(Resource):

    def get(self, contact_id):  
        resumes = resume.query.filter_by(contact_id=contact_id).order_by(Resume.date_created.desc())
        res_list = resumes_schema.dump(resumes).data

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
        result = tag_schema.dump(res).data

        return {"status": 'success', 'data': result}, 201

class ResumeOne(Resource):

    def get(self, resume_id):
        res = Resume.query.filter_by(id=resume_id).first()

        if res:
            res_data = resume_schema.dump(res).data
            return {'status': 'success', 'data': res_data}, 200

    def delete(self, resume_id):
        res = Resume.query.filter_by(id=resume_id)
        if not res.first():
            return {'message': 'Resume does not exist'}, 400
        res.delete()
        db.session.commit()
        return {"status": 'success'}, 201

    def put(self, resume_id):
        res = Resume.query.filter_by(id=resume_id)

        if not res.first():
            return {'message': 'Resume does not exist'}, 400
        json_data = request.get_json(force=True)
        data, errors = resume_schema.load(json_data)
        if not data:
            return {'message': 'No data provided to update'}, 400
        res.update(data)
        db.session.commit()
        return {"status": 'success'}, 201


class ResumeSections(Resource):
    def get(self, resume_id):
        pass


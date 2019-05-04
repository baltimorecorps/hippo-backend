from flask_restful import Resource, request
from models.experience_model import Experience, ExperienceSchema, Type
from models.achievement_model import Achievement
from models.base_model import db

experience_schema = ExperienceSchema()
experiences_schema = ExperienceSchema(many=True)


class ExperienceAll(Resource):

    def get(self, contact_id):
        experiences = (Experience.query.filter_by(contact_id=contact_id)
                                       .order_by(Experience.date_end.desc(),
                                                 Experience.date_start.desc()))
        exp_list = experiences_schema.dump(experiences).data
        return {'status': 'success', 'data': exp_list}, 200

    def post(self, contact_id):
        json_data = request.get_json(force=True)
        data, errors = experience_schema.load(json_data)
        if not data:
            return {'message': 'No data provided to update'}, 400
        if errors:
            return errors, 422
        exp = Experience(**data)
        db.session.add(exp)
        db.session.commit()
        result = experience_schema.dump(exp).data
        return {"status": 'success', 'data': result}, 201

class ExperienceOne(Resource):

    def get(self, experience_id):
        exp = Experience.query.get(experience_id)
        if not exp:
            return {'message': 'Experience does not exist'}, 400
        exp_data = experience_schema.dump(exp).data
        return {'status': 'success', 'data': exp_data}, 200

    def delete(self, experience_id):
        exp = Experience.query.get(experience_id)
        if not exp:
            return {'message': 'Experience does not exist'}, 400
        exp.delete()
        db.session.commit()
        return {"status": 'success'}, 201

    def put(self, experience_id):
        exp = Experience.query.get(experience_id)
        if not exp:
            return {'message': 'Experience does not exist'}, 400
        json_data = request.get_json(force=True)
        data, errors = experience_schema.load(json_data)
        if not data:
            return {'message': 'No data provided to update'}, 400
        for k,v in data.items():
            setattr(exp, k, v)
        result = experience_schema.dump(exp).data
        db.session.commit()
        return {'status': 'success', 'data': result}, 201

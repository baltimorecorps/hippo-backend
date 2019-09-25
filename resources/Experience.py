from flask_restful import Resource, request
from models.experience_model import Experience, ExperienceSchema, Type
from models.achievement_model import Achievement, AchievementSchema
from models.base_model import db
import datetime as dt
from operator import attrgetter

experience_schema = ExperienceSchema()
experiences_schema = ExperienceSchema(many=True)
type_list = [m for m in Type.__members__.keys()]


class ExperienceAll(Resource):

    def get(self, contact_id):
        type_arg = request.args.get('type')
        if type_arg:
            if type_arg not in Type.__members__:
                return {'message':
                        f'No such experience type, '
                        f'choose an option from this list: {type_list}'}, 400
            exp = (Experience.query.filter_by(contact_id=contact_id,
                                              type=Type[type_arg]))
        else:
            exp = (Experience.query.filter_by(contact_id=contact_id))
        exp_sorted = sorted(exp,
                            key=attrgetter('date_end', 'date_start'),
                            reverse=True)
        exp_list = experiences_schema.dump(exp_sorted).data
        return {'status': 'success', 'data': exp_list}, 200

    def post(self, contact_id):
        json_data = request.get_json(force=True)
        data, errors = experience_schema.load(json_data)
        if not data:
            return {'message': 'No data provided to update'}, 400
        if errors:
            return errors, 422

        #pull out the achievements to create them later
        achievements = data.pop('achievements', None)

        #create the experience record
        exp = Experience(**data)
        if achievements:
            for achievement in achievements:
                a = Achievement(**achievement)
                a.contact_id = exp.contact_id
                exp.achievements.append(a)
        db.session.add(exp)
        db.session.commit()
        result = experience_schema.dump(exp).data
        return {"status": 'success', 'data': result}, 201

class ExperienceOne(Resource):

    def get(self, experience_id):
        exp = Experience.query.get(experience_id)
        if not exp:
            return {'message': 'Experience does not exist'}, 404
        exp_data = experience_schema.dump(exp).data
        return {'status': 'success', 'data': exp_data}, 200

    def delete(self, experience_id):
        exp = Experience.query.get(experience_id)
        if not exp:
            return {'message': 'Experience does not exist'}, 404
        db.session.delete(exp)
        db.session.commit()
        return {"status": 'success'}, 200

    def put(self, experience_id):
        exp = Experience.query.get(experience_id)
        if not exp:
            return {'message': 'Experience does not exist'}, 404
        json_data = request.get_json(force=True)
        data, errors = experience_schema.load(json_data, partial=True)
        if not data:
            return {'message': 'No data provided to update'}, 400
        if errors:
            return errors, 422

        achievements = data.pop('achievements', None)

        for k,v in data.items():
            setattr(exp, k, v)
        del exp.achievements[:]
        if achievements:
            for achievement in achievements:
                a = Achievement(**achievement)
                a.contact_id = exp.contact_id
                exp.achievements.append(a)
        db.session.commit()
        result = experience_schema.dump(exp).data
        return {'status': 'success', 'data': result}, 200

from flask_restful import Resource, request
from models.experience_model import Experience, ExperienceSchema, Type
from models.achievement_model import Achievement, AchievementSchema
from models.base_model import db
import datetime as dt

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
            exp = (Experience.query
                             .filter_by(contact_id=contact_id,
                                        type=Type[type_arg])
                             .order_by(Experience.date_end.desc(),
                                       Experience.date_start.desc()))
        else:
            exp = (Experience.query
                             .filter_by(contact_id=contact_id)
                             .order_by(Experience.date_end.desc(),
                                       Experience.date_start.desc()))
        exp_list = experiences_schema.dump(exp).data
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

        #pull out the fields to store experience dates
        start_month = data.pop('start_month', None)
        start_year = data.pop('start_year', None)
        end_month = data.pop('end_month', None)
        end_year = data.pop('end_year', None)

        #generate experience dates
        if start_month and start_year:
            start_str = f'1 {start_month}, {start_year}'
            start_dt = dt.datetime.strptime(start_str,'%d %B, %Y')
            data['date_start'] = start_dt.date()
        if end_month and end_year:
            end_str = f'1 {end_month}, {end_year}'
            end_dt = dt.datetime.strptime(end_str,'%d %B, %Y')
            data['date_end'] = end_dt.date()

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

        #pull out the fields to store experience dates
        start_month = data.pop('start_month', None)
        start_year = data.pop('start_year', None)
        end_month = data.pop('end_month', None)
        end_year = data.pop('end_year', None)

        #generate experience dates
        if start_month and start_year:
            start_str = f'1 {start_month}, {start_year}'
            start_dt = dt.datetime.strptime(start_str,'%d %B, %Y')
            data['date_start'] = start_dt.date()
        if end_month and end_month:
            end_str = f'1 {end_month}, {end_year}'
            end_dt = dt.datetime.strptime(end_str,'%d %B, %Y')
            data['date_end'] = end_dt.date()

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

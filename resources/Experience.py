from flask_restful import Resource, request
from models.experience_model import Experience, ExperienceSchema, Type
from models.achievement_model import Achievement
from models.base_model import db

experience_schema = ExperienceSchema()
experiences_schema = ExperienceSchema(many=True)


class ExperienceAll(Resource):

    def get(self, contact_id):
        experiences = Experience.query.filter_by(contact_id=contact_id).order_by(Experience.date_end.desc(),
                                                                                 Experience.date_start.desc())
        exp_list = experiences_schema.dump(experiences).data

        return {'status': 'success', 'data': exp_list}, 200


class ExperienceOne(Resource):

    def get(self, contact_id, experience_id):
        exp = Experience.query.filter_by(contact_id=contact_id).filter_by(id=experience_id).first()

        if exp:
            exp_data = experience_schema.dump(exp).data
            return {'status': 'success', 'data': exp_data}, 200

    def post(self, contact_id):

        json_data = request.get_json(force=True)

        if not json_data:
            return {'message': 'No input data provided'}, 400
        json_data['contact_id'] = contact_id

        # Validate and deserialize input
        data, errors = experience_schema.load(json_data)
        if errors:
            return errors, 422

        achievements = []

        if 'achievements' in data:
            achievements = data.pop('achievements')
            data['achievements'] = []

        exp = Experience(**data)

        for achievement in achievements:
            # Create email object and append to contact email field
            exp.achievements.append(Achievement(**achievement))

        db.session.add(exp)
        db.session.commit()
        result = experience_schema.dump(exp).data

        return {"status": 'success', 'data': result}, 201

    def delete(self, contact_id, experience_id):
        exp = Experience.query.with_entities(Experience.id, Experience.description, Experience.host,
                                                     Experience.title, Experience.date_start, Experience.date_end,
                                                     Experience.type)\
                        .filter_by(contact_id=contact_id)\
                        .filter_by(id=experience_id)
        if not exp.first():
            return {'message': 'Experience does not exist'}, 400
        exp.delete()
        db.session.commit()
        return {"status": 'success'}, 201

    def put(self, contact_id, experience_id):
        exp = Experience.query.filter_by(contact_id=contact_id).filter_by(id=experience_id)

        if not exp.first():
            return {'message': 'Experience does not exist'}, 400
        json_data = request.get_json(force=True)
        data, errors = experience_schema.load(json_data)
        if not data:
            return {'message': 'No data provided to update'}, 400

        achievements = []
        if 'achievements' in data:
            achievements = data.pop('achievements')

        for achievement in achievements:
            # Check if any achievement was updated
            try:
                ach = Achievement.query.filter_by(exp_id=experience_id).filter_by(id=achievement['id'])
                if not ach.first():
                    return {'message': 'Incorrect id. This achievement does not exist!'}, 400
                else:
                    ach.update(achievement)
            except:
                return {'message': 'Did not provide achievement id'}, 400

        # q = dict((k, [Achievement(**x) for x in v]) if k == 'achievements' else (k, v) for k, v in data.items())

        exp.update(data)
        db.session.commit()
        return {"status": 'success'}, 201


class ExperienceList(Resource):
    def post(self, contact_id):
        json_data = request.get_json(force=True)

        if not json_data:
            return {'message': 'No input data provided'}, 400

        for d in json_data:
            d['contact_id'] = contact_id
        # Validate and deserialize input
        data, errors = experiences_schema.load(json_data)
        if errors:
            return errors, 422
        result = []
        for exp_data in data:
            achievements = []
            if 'achievements' in exp_data:
                achievements = exp_data.pop('achievements')
                exp_data['achievements'] = []
            exp = Experience(**exp_data)

            for achievement in achievements:
                # Create email object and append to contact email field
                exp.achievements.append(Achievement(**achievement))

            db.session.add(exp)
            db.session.commit()
            result.append(experience_schema.dump(exp).data)

        return {"status": 'success', 'data': result}, 201


class ExperienceType(Resource):
    def get(self, contact_id, exp_type):
        type_str = exp_type.strip().lower()
            
        if Type.work.value.lower() == type_str:
            type = Type.work
        elif Type.service.value.lower() == type_str:
            type = Type.service
        elif Type.accomplishment.value.lower() == type_str:
            type = Type.accomplishment
        elif Type.education.value.lower() == type_str:
            type = Type.education
        else:
            return {'message': 'No such experience type'}, 400

        exp = Experience.query.filter_by(contact_id=contact_id).filter_by(type=type).order_by(Experience.date_end.desc(),
                                                                                 Experience.date_start.desc())


        if exp:
            exp_data = experiences_schema.dump(exp).data
            return {'status': 'success', 'data': exp_data}, 200

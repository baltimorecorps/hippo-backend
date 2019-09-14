from flask_restful import Resource, request
from models.resume_model import Resume, ResumeSchema
from models.resume_section_model import ResumeSection, ResumeSectionSchema
from models.resume_item_model import ResumeItem, ResumeItemSchema
from models.base_model import db

resumes_schema = ResumeSchema(many=True)
resume_schema = ResumeSchema()

resume_sections_schema = ResumeSectionSchema(many=True)
resume_section_schema = ResumeSectionSchema()

class ResumeAll(Resource):

    def get(self, contact_id):
        res = Resume.query.filter_by(contact_id=contact_id)
        res_list = resumes_schema.dump(res).data
        return {'status': 'success', 'data': res_list}, 200

    def post(self, contact_id):
        json_data = request.get_json(force=True)
        data, errors = resume_schema.load(json_data)
        if not data:
            return {'message': 'No input data provided'}, 400
        if errors:
            return errors, 422
        res = Resume(**data)
        db.session.add(res)
        db.session.commit()
        result = resume_schema.dump(res).data
        return {'status': 'success', 'data': result}, 201

class ResumeOne(Resource):

    def get(self, resume_id):
        res = Resume.query.get(resume_id)
        if not res:
            return {'message': 'Resume does not exist'}, 404
        result = resume_schema.dump(res).data
        return {'status': 'success', 'data': result}, 200

    def delete(self, resume_id):
        res = Resume.query.get(resume_id)
        if not res:
            return {'message': 'Resume does not exist'}, 404
        db.session.delete(res)
        db.session.commit()
        return {'status': 'success'}, 200

    def put(self, resume_id):
        res = Resume.query.get(resume_id)
        if not res:
            return {'message': 'Resume does not exist'}, 404
        json_data = request.get_json(force=True)
        data, errors = resume_schema.load(json_data, partial=True)
        if not data:
            return {'message': 'No data provided to update'}, 400
        if errors:
            return errors, 422
        for k,v in data.items():
            setattr(res, k, v)
        db.session.commit()
        result = resume_schema.dump(res).data
        return {'status': 'success', 'data': result}, 200

class ResumeSectionAll(Resource):
    def get(self, resume_id):
        sections = ResumeSection.query.filter_by(resume_id=resume_id)
        result = resume_sections_schema.dump(sections).data
        return {'status': 'success', 'data': result}, 200

    def post(self, resume_id):
        json_data = request.get_json(force=True)
        data, errors = resume_section_schema.load(json_data)
        if not data:
            return {'message': 'No input data provided'}, 400
        if errors:
            return errors, 422
        items = data.pop('items', None)
        section = ResumeSection(**data)
        if items:
            for item in items:
                i = ResumeItem(**item)
                i.resume_id = section.resume_id
                section.items.append(i)
        db.session.add(section)
        db.session.commit()
        result = resume_section_schema.dump(section).data
        return {'status': 'success', 'data': result}, 201

class ResumeSectionOne(Resource):

    def get(self, resume_id, section_id):
        section = ResumeSection.query.get(section_id)
        if not section:
            return {'message': 'Resume section does not exist'}, 404
        result = resume_section_schema.dump(section).data
        return {'status': 'success', 'data': result}, 200

    def put(self, resume_id, section_id):
        section = ResumeSection.query.get(section_id)
        if not section:
            return {'message': 'Resume section does not exist'}, 404
        json_data = request.get_json(force=True)
        data, errors = resume_section_schema.load(json_data, partial=True)
        if not data:
            return {'message': 'No input data provided'}, 400
        if errors:
            return errors, 422
        items = data.pop('items', None)
        for k,v in data.items():
            setattr(section, k, v)
        del section.items[:]
        if items:
            for item in items:
                i = ResumeItem(**item)
                i.resume_id = section.resume_id
                section.items.append(i)
        db.session.commit()
        result = resume_section_schema.dump(section).data
        return {'status': 'success', 'data': result}, 200

    def delete(self, resume_id, section_id):
        section = ResumeSection.query.get(section_id)
        if not section:
            return {'message': 'Resume section does not exist'}, 404
        db.session.delete(section)
        db.session.commit()
        return {'status': 'success'}, 200

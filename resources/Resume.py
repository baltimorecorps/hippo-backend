from flask_restful import Resource, request
from models.resume_model import Resume, ResumeSchema
from models.resume_section_model import ResumeSection, ResumeSectionSchema
from models.resume_item_model import ResumeItem, ResumeItemSchema
from models.base_model import db

resumes_schema = ResumeSchema(many=True)
resume_schema = ResumeSchema(exclude=['sections'])
resume_render_schema = ResumeSchema()

resume_sections_schema = ResumeSectionSchema(many=True)
resume_section_schema = ResumeSectionSchema()

resume_items_schema = ResumeItemSchema(many=True)
resume_item_schema_load = ResumeItemSchema(exclude=['experience',
                                                    'tag',
                                                    'achievement'])
resume_item_schema_dump = ResumeItemSchema(exclude=['exp_id',
                                                    'tag_id',
                                                    'achievement_id'])

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
            return {'message': 'Resume does not exist'}, 400
        result = resume_render_schema.dump(res).data
        return {'status': 'success', 'data': result}, 200

    def delete(self, resume_id):
        res = Resume.query.get(resume_id)
        if not res.first():
            return {'message': 'Resume does not exist'}, 400
        res.delete()
        db.session.commit()
        return {'status': 'success'}, 201

    def put(self, resume_id):
        res = Resume.query.get(resume_id)
        if not res:
            return {'message': 'Resume does not exist'}, 400
        json_data = request.get_json(force=True)
        data, errors = resume_schema.load(json_data)
        if not data:
            return {'message': 'No data provided to update'}, 400
        if errors:
            return errors, 422
        for k,v in data.items():
            setattr(res, k, v)
        db.session.commit()
        result = resume_schema.dump(res)
        return {'status': 'success', 'data': result}, 201

class ResumeSectionAll(Resource):
    def get(self, resume_id):
        sections = ResumeSection.query.filter(resume_id=resume_id)
        res_list = resume_sections_schema.dump(res).data
        return {'status': 'success', 'data': res_list}, 200

    def post(self, resume_id):
        json_data = request.get_json(force=True)
        data, errors = resume_section_schema.load(json_data)
        if not data:
            return {'message': 'No input data provided'}, 400
        if errors:
            return errors, 422
        section = ResumeSection(**data)
        db.session.add(section)
        db.session.commit()
        result = resume_schema.dump(section).data
        return {'status': 'success', 'data': result}, 201

class ResumeSectionOne(Resource):

    def get(self, section_id):
        section = ResumeSection.query.get(section_id)
        if not section:
            return {'message': 'Resume section does not exist'}, 400
        result = resume_section_schema.dump(section)
        return {'status': 'success', 'data': result}, 201

class ResumeItemAll(Resource):

    def post(self, resume_id, section_id):
        json_data = request.get_json(force=True)
        data, errors = resume_item_schema_load.load(json_data)
        if not data:
            return {'message': 'No input data provided'}, 400
        if errors:
            return errors, 422
        item = ResumeItem(**data)
        db.session.add(item)
        db.session.commit()
        result = resume_item_schema_dump.dump(item).data
        return {'status': 'success', 'data': result}, 201

class ResumeItemOne(Resource):

    def put(self, resume_id, section_id, item_position):
        item = ResumeItem.query.filter_by(section_id=section_id,
                                          resume_order=item_position).first()
        if not item:
            return {'message': 'Item does not exist'}
        json_data = request.get_json(force=True)
        data, errors = resume_item_schema_load.load(json_data)
        if not data:
            return {'message': 'No data provided to update'}, 400
        if errors:
            return errors, 422
        for k,v in data.items():
            setattr(item, k, v)
        db.session.commit()
        result = resume_item_schema_dump.dump(item)
        return {'status': 'success', 'data': result}, 201

    def delete(self, resume_id, section_id, item_position):
        item = ResumeItem.query.filter_by(section_id=section_id,
                                          resume_order=item_position).first()
        if not item:
            return {'message': 'Item does not exist'}
        db.session.delete(item)
        db.session.commit()
        return {'status': 'success'}, 201

class ResumeItemReorder(Resource):

    def patch(self, resume_id, section_id, item_position):
        pass
        '''
        Not sure if it would make sense to implement an endpoint like this
        but I was thinking this could be used to efficiently update
        the order of the items in a section by following the strategy
        suggested in this post:
        https://softwareengineering.stackexchange.com/questions/195308/storing-a-re-orderable-list-in-a-database
        for the time being, this same functionality can be supported by
        simply PUTting to each of the items in the section
        '''

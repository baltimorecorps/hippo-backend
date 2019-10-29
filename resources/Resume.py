from flask_restful import Resource, request
from models.resume_model import Resume, ResumeSchema, ResumeSchemaNew
from models.resume_section_model import ResumeSection, ResumeSectionSchema
from models.resume_item_model import ResumeItem, ResumeItemSchema
from models.contact_model import Contact
from models.experience_model import Experience
from models.tag_item_model import TagItem
from models.base_model import db
from .generate_resume import generate
from marshmallow import ValidationError
import datetime as dt
from pprint import pprint

resumes_schema = ResumeSchema(many=True)
resume_schema = ResumeSchema()
resume_generate_schema = ResumeSchemaNew()
resume_output_schema = ResumeSchemaNew(only=['id', 'name','date_created', 'gdoc_id'])

resume_sections_schema = ResumeSectionSchema(many=True)
resume_section_schema = ResumeSectionSchema()

class GenerateResume(Resource):

    def post(self, contact_id):
        #load the input data
        input_data = request.get_json(force=True)
        try:
            data = resume_generate_schema.load(input_data)
        except ValidationError as e:
            return e.messages, 422
        if not data:
            return {'message': 'No input data provided'}, 400

        #pop off the ids for the data in each of the sections
        relevant_exp = data.pop('relevant_exp', None)
        other_exp = data.pop('other_exp', None)
        relevant_edu = data.pop('relevant_edu', None)
        other_edu = data.pop('other_edu', None)
        relevant_achieve = data.pop('relevant_achieve', None)
        other_achieve = data.pop('other_achieve', None)
        relevant_skills = data.pop('relevant_skills', None)
        other_skills = data.pop('other_skills', None)

        #query and add contact info to input data
        data['contact'] = Contact.query.get(contact_id)

        #query subset of resume items using lists of ids then
        #add those items to the input data with their section name
        def query_by_ids(table, id_list, contact_id, section_name):
            result = table.query.filter(table.id.in_(id_list),
                                        table.contact_id==contact_id)
            data[section_name] = result

        query_by_ids(Experience, relevant_exp, contact_id, 'relevant_exp_dump')
        query_by_ids(Experience, other_exp, contact_id, 'other_exp_dump')
        query_by_ids(Experience, relevant_edu, contact_id, 'relevant_edu_dump')
        query_by_ids(Experience, other_edu, contact_id, 'other_edu_dump')
        query_by_ids(Experience, relevant_achieve, contact_id, 'relevant_achieve_dump')
        query_by_ids(Experience, other_achieve, contact_id, 'other_achieve_dump')
        query_by_ids(TagItem, relevant_skills, contact_id, 'relevant_skills_dump')
        query_by_ids(TagItem, other_skills, contact_id, 'other_skills_dump')

        #dumps the throughput data and pass to generate resume script
        throughput_data = resume_generate_schema.dump(data)
        pprint(throughput_data)
        gdoc_id = generate(throughput_data)

        #creates dictionary to insert new resume record
        output_data = {
            'name': data['name'],
            'date_created': dt.datetime.today(),
            'contact_id': contact_id,
            'gdoc_id': gdoc_id,
        }
        resume = Resume(**output_data)
        db.session.add(resume)
        db.session.commit()
        result = resume_output_schema.dump(resume)
        return {'status': 'success', 'data': result}, 201

class ResumeAll(Resource):

    def get(self, contact_id):
        res = Resume.query.filter_by(contact_id=contact_id)
        res_list = resumes_schema.dump(res)
        return {'status': 'success', 'data': res_list}, 200

    def post(self, contact_id):
        json_data = request.get_json(force=True)
        try:
            data = resume_schema.load(json_data)
        except ValidationError as e:
            return e.messages, 422
        if not data:
            return {'message': 'No input data provided'}, 400
        res = Resume(**data)
        db.session.add(res)
        db.session.commit()
        result = resume_schema.dump(res)
        return {'status': 'success', 'data': result}, 201

class ResumeOne(Resource):

    def get(self, resume_id):
        res = Resume.query.get(resume_id)
        if not res:
            return {'message': 'Resume does not exist'}, 404
        from models.tag_item_model import TagItemSchema
        ris = ResumeItemSchema()
        tis = TagItemSchema()
        print(tis.dump(res.sections[1].items[0].tag))
        result = resume_schema.dump(res)
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
        try:
            data = resume_schema.load(json_data, partial=True)
        except ValidationError as e:
            return e.messages, 422
        if not data:
            return {'message': 'No data provided to update'}, 400
        for k,v in data.items():
            setattr(res, k, v)
        db.session.commit()
        result = resume_schema.dump(res)
        return {'status': 'success', 'data': result}, 200

class ResumeSectionAll(Resource):
    def get(self, resume_id):
        sections = ResumeSection.query.filter_by(resume_id=resume_id)
        result = resume_sections_schema.dump(sections)
        return {'status': 'success', 'data': result}, 200

    def post(self, resume_id):
        json_data = request.get_json(force=True)
        try:
            data = resume_section_schema.load(json_data)
        except ValidationError as e:
            return e.messages, 422
        if not data:
            return {'message': 'No input data provided'}, 400
        items = data.pop('items', None)
        section = ResumeSection(**data)
        if items:
            for item in items:
                i = ResumeItem(**item)
                i.resume_id = section.resume_id
                section.items.append(i)
        db.session.add(section)
        db.session.commit()
        result = resume_section_schema.dump(section)
        return {'status': 'success', 'data': result}, 201

class ResumeSectionOne(Resource):

    def get(self, resume_id, section_id):
        section = ResumeSection.query.get(section_id)
        if not section:
            return {'message': 'Resume section does not exist'}, 404
        result = resume_section_schema.dump(section)
        return {'status': 'success', 'data': result}, 200

    def put(self, resume_id, section_id):
        section = ResumeSection.query.get(section_id)
        if not section:
            return {'message': 'Resume section does not exist'}, 404
        json_data = request.get_json(force=True)
        try:
            data = resume_section_schema.load(json_data, partial=True)
        except ValidationError as e:
            return e.messages, 422
        if not data:
            return {'message': 'No input data provided'}, 400
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
        result = resume_section_schema.dump(section)
        return {'status': 'success', 'data': result}, 200

    def delete(self, resume_id, section_id):
        section = ResumeSection.query.get(section_id)
        if not section:
            return {'message': 'Resume section does not exist'}, 404
        db.session.delete(section)
        db.session.commit()
        return {'status': 'success'}, 200

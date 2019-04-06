from flask_restful import Resource, request
from models.tag_model import Tag, TagSchema, TagItem, TagItemSchema
from models.contact_model import Contact, ContactSchema
from models.base_model import db


contacts_schema = ContactSchema(many=True)
tag_schema = TagSchema()
tags_schema = TagSchema(many=True)
tagitem_schema = TagItemSchema()

class TagAll(Resource):

	def get(self):
		tags = Tag.query.with_entities(Tag.id, Tag.name, Tag.type)
		tags_list = tags_schema.dump(tags).data

		return {'status': 'success', 'data': tags_list}, 200


class TagOne(Resource):

	def get(self, tag_id):
		tags_list = Tag.query.with_entities(Tag.id, Tag.name, Tag.type)\
						.filter_by(id=tag_id)
		
		if not tags_list.first():
			return {'message': 'Tag does not exist'}, 400

		tag = tag_schema.dump(tags_list.first()).data

		return {'status': 'success', 'data': tag}, 200


	def post(self, tag_id):
		json_data = request.get_json(force=True)

		if not json_data:
			return {'message': 'No input data provided'}, 400

		# Validate and deserialize input
		data, errors = tag_schema.load(json_data)
		if errors:
			return errors, 422

		tag = Tag(**data)

		db.session.add(tag)
		db.session.commit()
		result = tag_schema.dump(tag).data

		return {"status": 'success', 'data': result}, 201


	def delete(self, tag_id):
		tag = Tag.query.with_entities(Tag.id, Tag.name, Tag.type, Tag.status)\
						.filter_by(id=tag_id)
		if not tag.first():
			return {'message': 'Tag does not exist'}, 400
		tag.delete()
		db.session.commit()
		return {"status": 'success'}, 201


	def put(self, tag_id):
		tag = Tag.query.with_entities(Tag.id, Tag.name, Tag.type, Tag.status)\
						.filter_by(id=tag_id)
		if not tag.first():
			return {'message': 'Tag does not exist'}, 400
		json_data = request.get_json(force=True)
		data, errors = tag_schema.load(json_data)
		if not data:
			return {'message': 'No data provided to update'}, 400
		tag.update(data)
		db.session.commit()
		return {"status": 'success'}, 201


class ContactWithThisTagSearch(Resource):

	def get(self, tag_id):
		contacts = Contact.query.join(TagItem, Contact.id==TagItem.contact_id) \
						.filter_by(id=tag_id) \
						.with_entities(Tag,Contact.id, Contact.first_name, Contact.last_name, Contact.email_primary)

		contacts_data = contacts_schema.dump(contacts).data
		return {'status': 'success', 'data': contacts_data}, 200
		


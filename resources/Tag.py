from flask_restful import Resource, request
from models.tag_model import Tag, TagSchema, TagStatusType, TagType
from models.tag_item_model import TagItem, TagItemSchema
from models.contact_model import Contact, ContactSchema
from models.base_model import db

# Useful for debugging
#from flask_sqlalchemy import get_debug_queries
#from pprint import pprint

tag_schema = TagSchema()
tags_schema = TagSchema(many=True)
tag_item_schema_load = TagItemSchema(exclude=['type', 'name'])
tag_item_schema_dump = TagItemSchema()
tag_items_schema = TagItemSchema(many=True)
type_list = [m for m in TagType.__members__.keys()]


# Returns a list of all tags
class TagAll(Resource):

    def get(self):
        tags = Tag.query.all()
        tags_list = tags_schema.dump(tags).data
        return {'status': 'success', 'data': tags_list}, 200

    def post(self):
        json_data = request.get_json(force=True)
        data, errors = tag_schema.load(json_data)
        if not data:
            return {'message': 'No data provided to update'}, 400
        if errors:
            return errors, 422
        tag = Tag(**data)
        db.session.add(tag)
        db.session.commit()
        result = tag_schema.dump(tag).data
        return {'status': 'success', 'data': result}, 201

# Returns a specific tag
class TagOne(Resource):

    def get(self, tag_id):
        tags_list = Tag.query.get(tag_id)
        if not tags_list.first():
            return {'message': 'Tag does not exist'}, 400
        tag = tag_schema.dump(tags_list.first()).data
        return {'status': 'success', 'data': tag}, 200

    def delete(self, tag_id):
        tag = Tag.query.get(tag_id)
        if not tag:
            return {'message': 'Tag does not exist'}, 400
        db.session.delete(tag)
        db.session.commit()
        return {'status': 'success'}, 201

    def put(self, tag_id):
        tag = Tag.query.get(tag_id)
        if not tag:
            return {'message': 'Tag does not exist'}, 400
        json_data = request.get_json(force=True)
        data, errors = tag_schema.load(json_data)
        if not data:
            return {'message': 'No data provided to update'}, 400
        if errors:
            return errors, 422
        for k,v in data.items():
            setattr(tag,k,v)
        db.session.commit()
        result = tag_schema.dump(tag).data
        return {'status': 'success', 'data': result}, 201


class TagItemAll(Resource):
    # returns a list of tags associated with a given contact
    def get(self, contact_id):
        type_arg = request.args.get('type')
        if type_arg:
            if type_arg not in TagType.__members__:
                return {'message':
                        f'No such tag type, '
                        f'choose an option from this list: {type_list}'}, 400
            tags = (TagItem.query.join(Tag)
                                 .filter(TagItem.contact_id==contact_id,
                                         Tag.type==TagType[type_arg]))
        else:
            tags = TagItem.query.filter_by(contact_id=contact_id)
        tags_list = tag_items_schema.dump(tags).data
        return {'status': 'success', 'data': tags_list}, 200

    def post(self, contact_id):
        json_data = request.get_json(force=True)
        data, errors = tag_item_schema_load.load(json_data)
        if not data:
            return {'message': 'No input data provided'}, 400
        if errors:
            return errors, 422
        tagitem = TagItem(**data)
        db.session.add(tagitem)
        db.session.commit()
        result = tag_item_schema_dump.dump(tagitem).data
        return {'status': 'success', 'data': result}, 201

class TagItemOne(Resource):
    def get(self, contact_id, tag_id):
        tag = (TagItem.query.filter_by(contact_id=contact_id, tag_id=tag_id)
                            .first())
        if not tag:
            return {'message': 'TagItem does not exist'}, 400
        tag_data = tag_item_schema_dump.dump(tag).data
        return {'status': 'success', 'data': tag_data}, 200

    def put(self, contact_id, tag_id):
        tag = (TagItem.query.filter_by(contact_id=contact_id, tag_id=tag_id)
                            .first())
        if not tag:
            return {'message': 'TagItem does not exist'}, 400
        json_data = request.get_json(force=True)
        data, errors = tag_item_schema_load.load(json_data)
        if not data:
            return {'message': 'No data provided to update'}, 400
        if errors:
            return errors, 422
        for k,v in data.items():
            if k in ('id', 'contact_id', 'tag_id'):
                continue
            setattr(tag, k, v)
        db.session.commit()
        result = tag_item_schema_dump.dump(tag)
        return {'status': 'success', 'data': result}, 201

    def delete(self, contact_id, tag_id):
        tag = TagItem.query.filter_by(contact_id=contact_id, tag_id=tag_id).first()
        if not tag:
            return {'message': 'TagItem does not exist'}, 400
        db.session.delete(tag)
        db.session.commit()
        return {'status': 'success'}, 201

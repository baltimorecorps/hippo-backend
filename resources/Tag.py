# TODO: DELETE THIS

from flask_restful import Resource, request
from models.tag_model import Tag, TagSchema, TagStatusType, TagType
from models.tag_item_model import TagItem, TagItemSchema
from models.contact_model import Contact
from models.base_model import db
from marshmallow import ValidationError

from flask_login import login_required
from auth import (
    refresh_session,
    is_authorized_view,
    is_authorized_write,
    unauthorized
)


# Useful for debugging
#from flask_sqlalchemy import get_debug_queries
#from pprint import pprint

tag_schema = TagSchema()
tags_schema = TagSchema(many=True)
tag_item_schema = TagItemSchema()
tag_items_schema = TagItemSchema(many=True)
type_list = [m for m in TagType.__members__.keys()]


# Returns a list of all tags
class TagAll(Resource):

    def get(self):
        tags = Tag.query.all()
        tags_list = tags_schema.dump(tags)
        return {'status': 'success', 'data': tags_list}, 200

    def post(self):
        json_data = request.get_json(force=True)
        try:
            data = tag_schema.load(json_data)
        except ValidationError as e:
            return e.messages, 422
        if not data:
            return {'message': 'No data provided to update'}, 400
        tag = Tag(**data)
        db.session.add(tag)
        db.session.commit()
        result = tag_schema.dump(tag)
        return {'status': 'success', 'data': result}, 201

# Returns a specific tag
class TagOne(Resource):


    def get(self, tag_id):
        tag = Tag.query.get(tag_id)
        if not tag:
            return {'message': 'Tag does not exist'}, 404
        result = tag_schema.dump(tag)
        return {'status': 'success', 'data': result}, 200

    def delete(self, tag_id):
        tag = Tag.query.get(tag_id)
        if not tag:
            return {'message': 'Tag does not exist'}, 404
        db.session.delete(tag)
        db.session.commit()
        return {'status': 'success'}, 201

    def put(self, tag_id):
        tag = Tag.query.get(tag_id)
        if not tag:
            return {'message': 'Tag does not exist'}, 404
        json_data = request.get_json(force=True)
        try:
            data = tag_schema.load(json_data, partial=True)
        except ValidationError as e:
            return e.messages, 422
        if not data:
            return {'message': 'No data provided to update'}, 400
        for k,v in data.items():
            setattr(tag,k,v)
        db.session.commit()
        result = tag_schema.dump(tag)
        return {'status': 'success', 'data': result}, 201


class TagItemAll(Resource):
    method_decorators = {
        'get': [login_required, refresh_session],
        'post': [login_required, refresh_session],
    }


    # returns a list of tags associated with a given contact
    def get(self, contact_id):
        if not is_authorized_view(contact_id):
            return unauthorized()

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
        tags_list = tag_items_schema.dump(tags)
        return {'status': 'success', 'data': tags_list}, 200

    def post(self, contact_id):
        if not is_authorized_write(contact_id):
            return unauthorized()

        json_data = request.get_json(force=True)
        try:
            data = tag_item_schema.load(json_data)
        except ValidationError as e:
            return e.messages, 422
        if not data:
            return {'message': 'No input data provided'}, 400
        tagitem = TagItem(**data)
        db.session.add(tagitem)
        db.session.commit()
        result = tag_item_schema.dump(tagitem)
        return {'status': 'success', 'data': result}, 201

class TagItemOne(Resource):
    method_decorators = {
        'get': [login_required, refresh_session],
        'put': [login_required, refresh_session],
        'delete': [login_required, refresh_session],
    }

    def get(self, contact_id, tag_id):
        if not is_authorized_view(contact_id):
            return unauthorized()

        tag = (TagItem.query.filter_by(contact_id=contact_id, tag_id=tag_id)
                            .first())
        if not tag:
            return {'message': 'TagItem does not exist'}, 404
        tag_data = tag_item_schema.dump(tag)
        return {'status': 'success', 'data': tag_data}, 200

    def put(self, contact_id, tag_id):
        if not is_authorized_write(contact_id):
            return unauthorized()

        tag = (TagItem.query.filter_by(contact_id=contact_id, tag_id=tag_id)
                            .first())
        if not tag:
            return {'message': 'TagItem does not exist'}, 404
        json_data = request.get_json(force=True)
        try:
            data = tag_item_schema.load(json_data, partial=True)
        except ValidationError as e:
            return e.messages, 422
        if not data:
            return {'message': 'No data provided to update'}, 400
        for k,v in data.items():
            setattr(tag, k, v)
        db.session.commit()
        result = tag_item_schema.dump(tag)
        return {'status': 'success', 'data': result}, 200

    def delete(self, contact_id, tag_id):
        if not is_authorized_write(contact_id):
            return unauthorized()

        tag = TagItem.query.filter_by(contact_id=contact_id, tag_id=tag_id).first()
        if not tag:
            return {'message': 'TagItem does not exist'}, 404
        db.session.delete(tag)
        db.session.commit()
        return {'status': 'success'}, 201

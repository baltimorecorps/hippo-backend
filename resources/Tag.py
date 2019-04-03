from flask_restful import Resource,request

class Tag(Resource):

    def get(self):
        pass


class TagItem(Resource):

    def get(self,tag_id):
        pass

    def post(self):
        pass


class ContactTags(Resource):

    def get(self,contact_id):
        pass

    def post(self, contact_id):
        pass

    def put(self,contact_id):
        pass


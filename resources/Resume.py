from flask_restful import Resource, request


class ContactsResume(Resource):

    def get(self, contact_id):  
        pass

    def post(self, contact_id):
        pass

class ResumeOne(Resource):

    def get(self, resume_id):
        pass

    def delete(self, resume_id):
        pass

    def put(self, resume_id):
        pass


class ResumeSections(Resource):
    def get(self, resume_id):
        pass


import json
from models.base_model import db
from marshmallow import Schema, fields, EXCLUDE, pre_load, post_dump


class ResumeSnapshot(db.Model):
    __tablename__ = 'resume_snapshot'
    id = db.Column(db.Integer, primary_key=True)
    resume = db.Column(db.Text, nullable=False)

class ResumeSnapshotSchema(Schema):
    resume = fields.String(required=True)

    @pre_load(pass_many=False)
    def pack_json(self, data, many, **kwargs):
        if 'resume' in data:
            data['resume'] = json.dumps(data['resume'], separators=(',',':'))
        return data

    @post_dump(pass_many=False)
    def unpack_json(self, data, many, **kwargs):
        if 'resume' in data:
            data['resume'] = json.loads(data['resume'])
        return data

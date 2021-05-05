import json

from marshmallow import Schema, fields, EXCLUDE, pre_load, post_dump


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

from models.base_model import db
from marshmallow import Schema, fields, post_dump, EXCLUDE
import datetime as dt
from models.program_model import Program


class Cycle(db.Model):

    #table columns
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('program.id'), nullable=False)
    date_start = db.Column(db.Date, nullable=False)
    date_end = db.Column(db.Date, nullable=False)
    intake_talent_board_id = db.Column(db.String)
    intake_org_board_id = db.Column(db.String)
    match_talent_board_id = db.Column(db.String)
    match_opp_board_id = db.Column(db.String)

    #relationship fields
    program = db.relationship('Program', back_populates='cycles')

    #calculated fields
    @hybrid_property
    def is_active(self):
        if self.date_end >= dt.date.today()
            return True
        else:
            return False

class Cycle(Schema):
    id = fields.String(dump_only=True)
    name = fields.Pluck(Program, 'name', attribute='program', dump_only=True)
    program_id = fields.String(required=True)
    is_active = fields.Boolean(dump_only=True)
    date_start = fields.Date()
    date_end = fields.Date()
    intake_talent_board_id = fields.String()
    intake_org_board_id = fields.String()
    match_talent_board_id = fields.String()
    match_opp_board_id = fields.String()

    class Meta:
        unknown = EXCLUDE

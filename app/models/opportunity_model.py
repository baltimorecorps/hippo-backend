import enum

from sqlalchemy.ext.hybrid import hybrid_property

from app.models import db, OpportunityApp


class OpportunityStage(enum.Enum):
    started = 0
    submitted = 1
    approved = 2
    posted = 3
    interviewing = 4
    filled = 5


class Opportunity(db.Model):
    __tablename__ = 'opportunity'

    # table columns
    id = db.Column(db.String, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    short_description = db.Column(db.String(2000), nullable=False)
    gdoc_id = db.Column(db.String(200))
    gdoc_link = db.Column(db.String(200), nullable=False)
    card_id = db.Column(db.String)
    program_name = db.Column(db.String)
    stage = db.Column(db.Integer, default=1)
    org_name = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # relationships
    applications = db.relationship('OpportunityApp', back_populates='opportunity',
                                   cascade='all, delete, delete-orphan')
    program = db.relationship('Program', back_populates='opportunities')

    @hybrid_property
    def status(self):
        return OpportunityStage(self.stage)

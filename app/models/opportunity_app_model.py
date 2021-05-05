import enum
import datetime as dt

from sqlalchemy.ext.hybrid import hybrid_property

from app.models import db

UPDATE_FIELDS = ['interest_statement',
                 'stage',
                 'interview_date',
                 'interview_time']


class ApplicationStage(enum.Enum):
    draft = 0
    submitted = 1
    recommended = 2
    interviewed = 3
    considered_for_role = 4


class OpportunityApp(db.Model):
    __tablename__ = 'opportunity_app'

    #table columns
    id = db.Column(db.String, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    opportunity_id = db.Column(db.String, db.ForeignKey('opportunity.id'), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume_snapshot.id'), nullable=True)
    interest_statement = db.Column(db.String(2000), nullable=True)
    stage = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    interview_date = db.Column(db.Date)
    interview_time = db.Column(db.String)

    resume = db.relationship('ResumeSnapshot')
    contact = db.relationship('Contact', back_populates='applications')

    opportunity = db.relationship('Opportunity')

    __table_args__ = (
        db.Index('oppapp_contact_opportunity',
                 'contact_id', 'opportunity_id', unique=True),
    )

    #calculated fields
    @hybrid_property
    def status(self):
        return ApplicationStage(self.stage)

    @hybrid_property
    def program_id(self):
        return self.opportunity.program_id

    @hybrid_property
    def interview_completed(self):
        if self.interview_date and self.interview_time:
            interview_scheduled = dt.datetime.strptime(
                f'{self.interview_date} {self.interview_time}',
                '%Y-%m-%d %H:%M:%S'
            )
            return interview_scheduled < dt.datetime.now()
        else:
            return False

    # for more info on why to use setattr() read this:
    # https://medium.com/@s.azad4/modifying-python-objects-within-the-sqlalchemy-framework-7b6c8dd71ab3
    def update(self, **update_dict):
        for field, value in update_dict.items():
            print(field, value)
            if field in UPDATE_FIELDS:
                setattr(self, field, value)

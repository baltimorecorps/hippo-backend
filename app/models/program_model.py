from app.models import db


class Program(db.Model):

    #table columns
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    trello_board_id = db.Column(db.String)

    #relationship fields
    program_apps = db.relationship('ProgramApp',
                                   back_populates='program',
                                   cascade='all, delete, delete-orphan')
    opportunities = db.relationship('Opportunity',
                               back_populates='program',
                               cascade='all, delete, delete-orphan')

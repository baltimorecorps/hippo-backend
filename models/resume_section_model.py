from models.base_model import db


class Resumesection(db.Model):
    __tablename__ = "resumesection"
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey("resume.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    min_count = db.Column(db.Integer)
    max_count = db.Column(db.Integer)
    resume = db.relationship('Resume')

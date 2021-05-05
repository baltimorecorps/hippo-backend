from app.models import db


class ResumeSnapshot(db.Model):
    __tablename__ = 'resume_snapshot'
    id = db.Column(db.Integer, primary_key=True)
    resume = db.Column(db.Text, nullable=False)

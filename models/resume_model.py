from models.base_model import db

class Resume(db.Model):
    __tablename__ = "resume"
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contact.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey("templates.id"), nullable=False)
    date_created = db.Column(db.Date, nullable=False)
    contact = db.relationship('Contact')
    templates = db.relationship('Templates')

from models.base_model import db


class Template(db.Model):
    __tablename__ = "template"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    template_url = db.Column(db.String(500), nullable=False)
    json = db.Column(db.String(500), nullable=False)

from models.base_model import db


class Templates(db.Model):
    __tablename__ = "templates"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    template_url = db.Column(db.String(500), nullable=False)
    json = db.Column(db.String(500), nullable=False)


from models.base_model import db


class ResumeItem(db.Model):
    __tablename__ = "resume_item"
    resume_order = db.Column(db.Integer,primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey("resume_section.id"), nullable=False, primary_key=True)
    exp_id = db.Column(db.Integer, db.ForeignKey("experience.id"), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag_item.id"), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey("experience.id"), nullable=False)
    indented = db.Column(db.Boolean, default=False)
    resume_section = db.relationship('ResumeSection')
    experience = db.relationship('Experience')
    tag_item = db.relationship('TagItem')

# TODO: DELETE THIS

from app import create_app
from models.base_model import db

from models.old_skill_model import SkillItem as OldSkillItem
from resources.skill_utils import get_or_make_skill

def migrate(db):
    old_items = OldSkillItem.query.all()
    for old_item in old_items:
        skill = get_or_make_skill(old_item.name)
        db.session.add(skill)
        old_item.contact.add_skill(skill)
        for exp in old_item.experiences:
            exp.add_skill(skill)
    db.session.commit()

def main():
    app = create_app('local')

    with app.app_context():
        db.init_app(app)
        migrate(db)

if __name__ == '__main__':
    main()

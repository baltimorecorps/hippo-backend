from app import create_app
from app.models.base_model import db

import common.add_skills as add_skills

def init_db():
    app = create_app('local')

    with app.app_context():
        db.init_app(app)
        add_skills.populate(db)

if __name__ == '__main__': 
    init_db()


from app import create_app
from models.base_model import db

def init_db():
    app = create_app()

    with app.app_context():
        db.init_app(app)
        db.create_all()

if __name__ == '__main__': 
    init_db()


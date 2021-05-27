from app import create_app
from app.models import db
from tests.populate_db import populate

def create_local_app():
    """Uses the application factory function to create a location version of
    the Flask app and populate a local db with sample data for manual testing
    """
    app = create_app()

    with app.app_context():
        db.drop_all()  # Drop existing tables
        db.create_all()  # Create sql tables for our data models
        populate()  # populates a local db with test data

    return app

if __name__ == "__main__":
    app = create_local_app()
    # allows us to access the app from within a docker container
    app.run(debug=True, host="0.0.0.0")

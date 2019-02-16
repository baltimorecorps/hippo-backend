from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from resources.Hello import Hello
from resources.Contacts import Contacts

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://:@localhost/mydb"

db = SQLAlchemy(app)

# Route
api.add_resource(Hello, '/Hello')
api.add_resource(Contacts, '/ContactsAll')

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)

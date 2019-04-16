from app import create_app
from flask_cors import CORS

if __name__ == "__main__":
    app = create_app("config")
    CORS(app)
    app.run(debug=True)

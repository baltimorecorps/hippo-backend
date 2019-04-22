from app import create_app
from flask_cors import CORS

<<<<<<< HEAD
app = create_app("config")
CORS(app)

if __name__ == "__main__":    
=======
if __name__ == "__main__":
    app = create_app("config")
    CORS(app)
>>>>>>> resume_model
    app.run(debug=True)

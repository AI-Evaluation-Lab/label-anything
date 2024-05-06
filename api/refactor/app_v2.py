from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from models import db, Image
from utils import initialize_images
from routes import setup_routes

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


setup_routes(app)


if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all()
        # initialize_images()
    app.run(debug=True)
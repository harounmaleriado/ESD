from flask import Flask
from main.models.auth_models import db
from main.routes.auth_routes import auth_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('main.config.Config')

    app.register_blueprint(auth_bp)

    return app

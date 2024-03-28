from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from main.models.auth_models import db
from main.routes.auth_routes import auth_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('main.config.Config')

    db.init_app(app)
    mail = Mail(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp)

    return app

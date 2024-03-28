from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from main.models.review_model import db
from main.routes.review_routes import review_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('main.config.Config')

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(review_bp)

    return app

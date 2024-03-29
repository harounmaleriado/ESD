from flask import Flask
from main.routes.listing_routes import listing_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(listing_bp)

    return app

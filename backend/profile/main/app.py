from flask import Flask
from main.routes.profile_routes import profile_bp
from main.message_receiver import start_message_receiver
from threading import Thread


def create_app():
    app = Flask(__name__)

    app.register_blueprint(profile_bp)

    t = Thread(target=lambda: start_message_receiver(app))
    t.daemon = True
    t.start()

    return app

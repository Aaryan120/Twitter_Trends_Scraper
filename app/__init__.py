from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
import os

load_dotenv()


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Load configuration
    app.config.from_object('app.config.Config')

    # Register routes
    from app.routes import main
    app.register_blueprint(main)

    return app
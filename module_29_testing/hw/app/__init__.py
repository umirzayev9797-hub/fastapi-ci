from flask import Flask
from .extensions import db


def create_app(config_object="config.Config"):
    app = Flask(__name__)

    app.config.from_object(config_object)

    db.init_app(app)

    return app

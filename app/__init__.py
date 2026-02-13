from flask import Flask

from .extensions import db
from .routes import bp


def create_app(config_object="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)

    app.register_blueprint(bp)

    return app

from flask import Flask

from app.extensions import db
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    from app import models  # noqa: F401

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app

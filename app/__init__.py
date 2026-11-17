from flask import Flask, render_template

from app.extensions import db
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    from app import models  # noqa: F401

    from app.routes import main
    from app.auth import auth
    from app.transactions import transactions

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(transactions)

    with app.app_context():
        db.create_all()

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    return app

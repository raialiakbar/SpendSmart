from datetime import datetime, timezone

from app.extensions import db


def utc_now():
    return datetime.now(timezone.utc)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    display_name = db.Column(db.String(64))
    currency = db.Column(db.String(3), nullable=False, default="EUR")
    created_at = db.Column(db.DateTime, nullable=False, default=utc_now)
    last_login_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"<User {self.username}>"

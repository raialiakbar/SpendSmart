import pytest

from app import create_app
from app.extensions import db
from app.models import User
from config import TestConfig


@pytest.fixture
def app():
    app = create_app(TestConfig)
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def create_user(app, username="alice", email="alice@example.com", password="secret123"):
    with app.app_context():
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user.id


def login(client, username="alice", password="secret123"):
    return client.post("/login", data={"username": username, "password": password})


@pytest.fixture
def logged_in_client(app, client):
    create_user(app)
    login(client)
    return client

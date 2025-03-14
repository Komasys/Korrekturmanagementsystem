from typing import Generator
import pytest
from flask import Flask
from flask.testing import FlaskClient
from models.models import db, Benutzer, Rolle
from app import app as flask_app

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

@pytest.fixture
def setup_user():
    """Hilfsfixure zur Erstellung eines Testbenutzers."""
    user = Benutzer(name='Test User', email='test@example.com', rolle=Rolle.STUDENT)
    user.set_password('password')
    db.session.add(user)
    db.session.commit()


def test_signup(client: FlaskClient):
    response = client.post('/auth/signup', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Benutzer erfolgreich registriert!'


def test_signup_existing_user(client: FlaskClient, setup_user):
    response = client.post('/auth/signup', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Benutzer existiert bereits!'


def test_signin(client: FlaskClient, setup_user):
    response = client.post('/auth/signin', json={
        'email': 'test@example.com',
        'password': 'password'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json


def test_signin_invalid_credentials(client: FlaskClient):
    response = client.post('/auth/signin', json={
        'email': 'nonexistent@example.com',
        'password': 'password'
    })
    assert response.status_code == 401
    assert response.json['message'] == 'Ungültige Anmeldedaten!'

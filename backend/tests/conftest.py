import sys
import os
import pytest

# Fügen Sie das Backend-Verzeichnis zum Python-Pfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'backend')))

# Setzen der Umgebungsvariable für die Datenbank-URL
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

from app import app as flask_app  # Importiere die Flask-App
from models import db

@pytest.fixture
def test_app():
    """Fixture für die Flask-App."""
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    flask_app.config['JWT_SECRET_KEY'] = 'test_secret_key'
    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(test_app):
    """Fixture für den Test-Client."""
    return test_app.test_client()

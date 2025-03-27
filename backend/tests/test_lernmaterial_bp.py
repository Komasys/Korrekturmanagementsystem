import pytest
from models import Lernmaterial, db
from uuid import uuid4, UUID
from datetime import datetime

@pytest.fixture
def sample_lernmaterial():
    """Fixture für Beispiel-Lernmaterialien."""
    kurs_id = uuid4()
    return kurs_id, [
        Lernmaterial(
            id=uuid4(),
            titel="Einführung in die Mathematik",
            typ="PDF",
            kurs_id=kurs_id,
            erstelldatum=datetime(2025, 3, 1, 10, 0, 0)  # Verwende datetime-Objekt
        ),
        Lernmaterial(
            id=uuid4(),
            titel="Fortgeschrittene Physik",
            typ="VIDEO",
            kurs_id=kurs_id,
            erstelldatum=datetime(2025, 3, 2, 12, 0, 0)  # Verwende datetime-Objekt
        ),
    ]

def test_get_lernmaterial_empty(client, test_app):
    """Testet den Endpunkt, wenn keine Lernmaterialien für den Kurs vorhanden sind."""
    kurs_id = uuid4()  # Verwende UUID-Objekt
    response = client.get(f'/lernmaterial/getLernmaterial/{kurs_id}')
    assert response.status_code == 200
    assert response.json == []

def test_get_lernmaterial_with_data(client, test_app, sample_lernmaterial):
    """Testet den Endpunkt, wenn Lernmaterialien für den Kurs in der Datenbank vorhanden sind."""
    kurs_id, lernmaterialien = sample_lernmaterial

    with test_app.app_context():
        db.session.add_all(lernmaterialien)
        db.session.commit()

        response = client.get(f'/lernmaterial/getLernmaterial/{kurs_id}')
        assert response.status_code == 200
        assert len(response.json) == len(lernmaterialien)
        assert response.json[0]["titel"] == "Einführung in die Mathematik"
        assert response.json[1]["typ"] == "video"

def test_get_lernmaterial_invalid_kurs_id(client):
    """Testet den Endpunkt mit einer ungültigen Kurs-ID."""
    invalid_kurs_id = uuid4()  # Verwende UUID-Objekt
    response = client.get(f'/lernmaterial/getLernmaterial/{invalid_kurs_id}')
    assert response.status_code == 200
    assert response.json == []
import pytest
from models import Kurs, db
from uuid import uuid4

@pytest.fixture
def sample_kurse():
    """Fixture für Beispielkurse."""
    return [
        Kurs(id=uuid4(), name="Mathematik", kuerzel="MATH"),
        Kurs(id=uuid4(), name="Physik", kuerzel="PHYS"),
    ]

def test_get_kurse_empty(client):
    """Testet den Endpunkt, wenn keine Kurse vorhanden sind."""
    response = client.get('/kurs/getKurse')
    assert response.status_code == 200
    assert response.json == []

def test_get_kurse_with_data(client, test_app, sample_kurse):
    """Testet den Endpunkt, wenn Kurse in der Datenbank vorhanden sind."""
    with test_app.app_context():
        db.session.add_all(sample_kurse)
        db.session.commit()

        response = client.get('/kurs/getKurse')
        assert response.status_code == 200
        assert len(response.json) == len(sample_kurse)
        assert response.json[0]["name"] == "Mathematik"
        assert response.json[1]["kuerzel"] == "PHYS"
import pytest
from models import db, Ticket, Benutzer, Kurs, Kategorie, TicketStatus, Prioritaet
from datetime import datetime, timezone

@pytest.fixture
def sample_user(test_app):
    """Fixture for creating a sample user."""
    user = Benutzer(name="Test User", email="test@example.com", rolle="STUDENT")
    user.password = "password"
    with test_app.app_context():
        db.session.add(user)
        db.session.commit()
        return user.id  # Return the user ID

@pytest.fixture
def sample_kurs(test_app, sample_user):
    """Fixture for creating a sample course."""
    kurs = Kurs(name="Test Kurs", kuerzel="TEST", kursleitung_id=sample_user)
    with test_app.app_context():
        db.session.add(kurs)
        db.session.commit()
        return kurs.id  # Return the course ID

def test_set_ticket(client, test_app, sample_user, sample_kurs):
    """Test creating a new ticket."""
    data = {
        "beschreibung": "Test Ticket Beschreibung",
        "kategorie": Kategorie.TIPPFEHLER.name,
        "kurs_id": sample_kurs,
        "benutzer_id": sample_user,
    }
    response = client.post("/ticket/setTicket", data=data)
    assert response.status_code == 201
    assert response.json["message"] == "Ticket erfolgreich eingereicht!"

def test_get_ticket(client, test_app, sample_user, sample_kurs):
    """Test retrieving a ticket by ID."""
    with test_app.app_context():
        ticket = Ticket(
            beschreibung="Test Ticket",
            kategorie=Kategorie.TIPPFEHLER,
            kurs_id=sample_kurs,
            ersteller_id=sample_user,
        )
        db.session.add(ticket)
        db.session.commit()
        ticket_id = ticket.id  # Access the ticket ID within the context

    response = client.get(f"/ticket/getTicket/{ticket_id}")
    assert response.status_code == 200
    assert response.json["beschreibung"] == "Test Ticket"
    assert response.json["kurs_name"] == "Test Kurs"

def test_get_all_tickets(client, test_app, sample_user, sample_kurs):
    """Test retrieving all tickets."""
    with test_app.app_context():
        ticket = Ticket(
            beschreibung="Test Ticket",
            kategorie=Kategorie.TIPPFEHLER,
            kurs_id=sample_kurs,
            ersteller_id=sample_user,
        )
        db.session.add(ticket)
        db.session.commit()

    response = client.get("/ticket/getAllTickets")
    assert response.status_code == 200
    assert len(response.json) > 0
    assert response.json[0]["beschreibung"] == "Test Ticket"

def test_update_ticket(client, test_app, sample_user, sample_kurs):
    """Test updating a ticket."""
    with test_app.app_context():
        ticket = Ticket(
            beschreibung="Test Ticket",
            kategorie=Kategorie.TIPPFEHLER,
            kurs_id=sample_kurs,
            ersteller_id=sample_user,
        )
        db.session.add(ticket)
        db.session.commit()
        ticket_id = ticket.id

    data = {
        "ticket_id": ticket_id,
        "status": TicketStatus.PRUEFUNG.value,
        "prioritaet": Prioritaet.HOCH.value,
        "beschreibung": "Updated Beschreibung",
        "bearbeiter_id": sample_user,
        "geaendert_am": datetime.now(timezone.utc)
    }
    response = client.post("/ticket/updateTicket", json=data)
    assert response.status_code == 200
    assert response.json["message"] == "Ticket aktualisiert!"

    with test_app.app_context():
        updated_ticket = db.session.get(Ticket, ticket_id)
        assert updated_ticket.prioritaet.value == "hoch"

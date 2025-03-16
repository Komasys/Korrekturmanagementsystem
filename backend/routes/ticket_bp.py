from flask import Blueprint, request, jsonify
from models.models import db, Ticket, Kategorie
ticket_bp = Blueprint('ticket_bp', __name__)

@ticket_bp.route('/setTicket', methods=['POST'])
def set_ticket():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Ungültige JSON-Daten!"}), 400

    new_ticket = Ticket(
        kategorie = data['kategorie'],
        kurs_id = data['kurs_id'],
        beschreibung = data['beschreibung'],
        ersteller_id = data['benutzer_id']
    )
    db.session.add(new_ticket)
    db.session.commit()

    return jsonify({'message': 'Ticket erfolgreich eingereicht!'}), 201

@ticket_bp.route('/getTicketKategorien', methods=['GET'])
def get_ticket_kategorien():
    def format_enum(enum_value):
        return enum_value.replace("_", " ").title()

    kategorie = {kategorie.name: format_enum(kategorie.name) for kategorie in Kategorie}
    return jsonify(kategorie), 200

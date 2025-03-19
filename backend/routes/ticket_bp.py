from flask import Blueprint, request, jsonify
from models import db, Ticket, Kategorie
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

@ticket_bp.route('/getTicket/<string:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({"message": "Ticket nicht gefunden!"}), 404

    return jsonify(ticket.serialize()), 200

@ticket_bp.route('/getAllTickets', methods=['GET'])
def get_all_tickets():
    tickets = Ticket.query.all()
    tickets = [ticket.serialize() for ticket in tickets]
    return jsonify(tickets), 200

@ticket_bp.route('/getTicketsByUser/<string:benutzer_id>', methods=['GET'])
def get_tickets_by_user(benutzer_id):
    tickets = Ticket.query.filter_by(ersteller_id=benutzer_id).all()
    tickets = [ticket.serialize() for ticket in tickets]
    return jsonify(tickets), 200

@ticket_bp.route('/getTicketKategorien', methods=['GET'])
def get_ticket_kategorien():
    def format_enum(enum_value):
        return enum_value.replace("_", " ").title()

    kategorie = {kategorie.name: format_enum(kategorie.name) for kategorie in Kategorie}
    return jsonify(kategorie), 200

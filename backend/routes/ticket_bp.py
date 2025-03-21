from flask import Blueprint, request, jsonify
from models import db, Ticket, Kategorie, Benutzer, Kurs, Historie, Kommentar
from datetime import datetime
ticket_bp = Blueprint('ticket_bp', __name__)

@ticket_bp.route('/setTicket', methods=['POST'])
def set_ticket():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Ungültige JSON-Daten!"}), 400

    new_ticket = Ticket(
        beschreibung = data['beschreibung'],
        kategorie = data['kategorie'],
        prioritaet = "NIEDRIG",
        kurs_id = data['kurs_id'],
        ersteller_id = data['benutzer_id'], ##########

    )
    db.session.add(new_ticket)
    db.session.commit()

    new_historie = Historie(
        ticket_id = new_ticket.id,
        status = "NEU",
        beschreibung = "*Ticket erstellt*",
        bearbeiter_id = data['benutzer_id'],
        geaendert_am = datetime.utcnow()
    )
    db.session.add(new_historie)
    db.session.commit()

    return jsonify({'message': 'Ticket erfolgreich eingereicht!'}), 201

@ticket_bp.route('/getTicket/<string:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({"message": "Ticket nicht gefunden!"}), 404

    user = Benutzer.query.get(ticket.ersteller_id)
    kurs = Kurs.query.get(ticket.kurs_id)
    ticket_status = Historie.query.filter_by(ticket_id=ticket_id).order_by(Historie.geaendert_am.desc()).first()
    kommentare = Kommentar.query.filter_by(ticket_id=ticket_id).all()
    historie = Historie.query.filter_by(ticket_id=ticket_id).all()

    ticket_data = ticket.serialize()
    ticket_data['ersteller_name'] = user.name if user else 'Unbekannt'
    ticket_data['kurs_name'] = kurs.name if kurs else 'Unbekannt'
    ticket_data['status'] = ticket_status.status.value if ticket_status else 'Unbekannt'
    ticket_data['kommentare'] = [kommentar.serialize() for kommentar in kommentare]
    ticket_data['historie'] = [eintrag.serialize() for eintrag in historie]

    # Include user names in comments
    for kommentar in ticket_data['kommentare']:
        benutzer = Benutzer.query.get(kommentar['benutzer_id'])
        kommentar['benutzer_name'] = benutzer.name if benutzer else 'Unbekannt'

    for eintrag in ticket_data['historie']:
        bearbeiter = Benutzer.query.get(eintrag['bearbeiter_id'])
        eintrag['bearbeiter_name'] = bearbeiter.name if bearbeiter else 'Unbekannt'

    return jsonify(ticket_data), 200

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

@ticket_bp.route('/addComment', methods=['POST'])
def add_comment():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Ungültige JSON-Daten!"}), 400

    benutzer_id = data.get('benutzer_id')
    if not benutzer_id:
        return jsonify({"message": "Benutzer-ID fehlt!"}), 400

    new_comment = Kommentar(
        benutzer_id=benutzer_id,
        ticket_id=data['ticket_id'],
        nachricht=data['nachricht']
    )
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({'message': 'Kommentar erfolgreich hinzugefügt!'}), 201

@ticket_bp.route('/updateTicket', methods=['POST'])
def update_ticket():
    data = request.json
    ticket_id = data.get('ticket_id')
    status = data.get('status')
    prioritaet = data.get('prioritaet')
    beschreibung = data.get('beschreibung')
    bearbeiter_id = data.get('bearbeiter_id')

    if not ticket_id or not status or not prioritaet:
        return jsonify({"message": "Fehlende Daten!"}), 400

    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({"message": "Ticket nicht gefunden!"}), 404

    historie = Historie(
        ticket_id=ticket_id,
        bearbeiter_id=bearbeiter_id,
        beschreibung=beschreibung,
        status=status,
        geaendert_am=datetime.utcnow()
    )

    ticket.prioritaet = prioritaet

    db.session.add(historie)
    db.session.commit()

    return jsonify({"message": "Ticket aktualisiert!"}), 200

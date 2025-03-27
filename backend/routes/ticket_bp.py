from flask import Blueprint, request, jsonify
from models import db, Ticket, Kategorie, Benutzer, Kurs, Historie, Kommentar, TicketStatus, Anhang, Prioritaet
from datetime import datetime, timezone
import os
from werkzeug.utils import secure_filename
import uuid
from sqlalchemy.orm import Session  # Add this import

ticket_bp = Blueprint('ticket_bp', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@ticket_bp.route('/setTicket', methods=['POST'])
def set_ticket():
    file = request.files.get('file')
    filename = None

    if file and file.filename != '':
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
        else:
            return jsonify({"message": "Ungültige Datei!"}), 400

    data = request.form.to_dict()
    if not data:
        return jsonify({"message": "Ungültige Formulardaten!"}), 400

    new_ticket = Ticket(
        beschreibung=data['beschreibung'],
        kategorie=data['kategorie'],
        prioritaet="NIEDRIG",
        kurs_id=uuid.UUID(data['kurs_id']),
        ersteller_id=uuid.UUID(data['benutzer_id'])
    )
    db.session.add(new_ticket)
    db.session.commit()

    if filename:
        new_anhang = Anhang(
            ticket_id=new_ticket.id,
            dateiname=filename
        )
        db.session.add(new_anhang)
        db.session.commit()

    new_historie = Historie(
        ticket_id=new_ticket.id,
        status="NEU",
        beschreibung="*Ticket erstellt*",
        bearbeiter_id=uuid.UUID(data['benutzer_id']),  # ← FIX
        geaendert_am=datetime.now(timezone.utc)
    )
    db.session.add(new_historie)
    db.session.commit()

    return jsonify({'message': 'Ticket erfolgreich eingereicht!'}), 201

@ticket_bp.route('/getTicket/<string:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    try:
        ticket_id = uuid.UUID(ticket_id)
    except ValueError:
        return jsonify({"message": "Ungültige Ticket-ID!"}), 400

    ticket = db.session.get(Ticket, ticket_id)
    if not ticket:
        return jsonify({"message": "Ticket nicht gefunden!"}), 404

    user = db.session.get(Benutzer, ticket.ersteller_id)
    kurs = db.session.get(Kurs, ticket.kurs_id)
    ticket_status = Historie.query.filter_by(ticket_id=ticket_id).order_by(Historie.geaendert_am.desc()).first()
    kommentare = Kommentar.query.filter_by(ticket_id=ticket_id).all()
    historie = Historie.query.filter_by(ticket_id=ticket_id).all()

    ticket_data = ticket.serialize()
    ticket_data['ersteller_name'] = user.name if user else 'Unbekannt'
    ticket_data['kurs_name'] = kurs.name if kurs else 'Unbekannt'
    ticket_data['status'] = ticket_status.status.value if ticket_status else 'Unbekannt'
    ticket_data['kommentare'] = [kommentar.serialize() for kommentar in kommentare]
    ticket_data['historie'] = [eintrag.serialize() for eintrag in historie]

    anhaenge = Anhang.query.filter_by(ticket_id=ticket_id).all()
    ticket_data['anhaenge'] = [anhang.serialize() for anhang in anhaenge]

    for kommentar in ticket_data['kommentare']:
        benutzer = Benutzer.query.get(uuid.UUID(kommentar['benutzer_id']))  # Convert string to UUID
        kommentar['benutzer_name'] = benutzer.name if benutzer else 'Unbekannt'

    for eintrag in ticket_data['historie']:
        bearbeiter = Benutzer.query.get(uuid.UUID(eintrag['bearbeiter_id']))  # Convert string to UUID
        eintrag['bearbeiter_name'] = bearbeiter.name if bearbeiter else 'Unbekannt'

    return jsonify(ticket_data), 200

@ticket_bp.route('/getAllTickets', methods=['GET'])
def get_all_tickets():
    tickets = Ticket.query.all()
    tickets = [ticket.serialize() for ticket in tickets]
    for ticket in tickets:
        ticket_id = uuid.UUID(ticket['id'])  # Convert string to UUID
        ticket_status = Historie.query.filter_by(ticket_id=ticket_id).order_by(Historie.geaendert_am.desc()).first()
        ticket['status'] = ticket_status.status.value if ticket_status else 'Unbekannt'
    return jsonify(tickets), 200

@ticket_bp.route('/getTicketsByUser/<string:benutzer_id>', methods=['GET'])
def get_tickets_by_user(benutzer_id):
    tickets = Ticket.query.filter_by(ersteller_id=benutzer_id).all()
    tickets = [ticket.serialize() for ticket in tickets]
    for ticket in tickets:
        ticket_status = Historie.query.filter_by(ticket_id=uuid.UUID(ticket['id'])).order_by(Historie.geaendert_am.desc()).first()
        ticket['status'] = ticket_status.status.value if ticket_status else 'Unbekannt'
    return jsonify(tickets), 200

@ticket_bp.route('/getTicketsByBearbeiter/<string:bearbeiter_id>', methods=['GET'])
def get_tickets_by_bearbeiter(bearbeiter_id):
    tickets = Ticket.query.join(Historie).filter(Historie.bearbeiter_id == bearbeiter_id).all()
    tickets = [ticket.serialize() for ticket in tickets]
    for ticket in tickets:
        ticket_status = Historie.query.filter_by(ticket_id=uuid.UUID(ticket['id'])).order_by(Historie.geaendert_am.desc()).first()
        ticket['status'] = ticket_status.status.value if ticket_status else 'Unbekannt'
    return jsonify(tickets), 200

@ticket_bp.route('/getTicketKategorien', methods=['GET'])
def get_ticket_kategorien():
    def format_enum(enum_value):
        return enum_value.replace("_", " ").title()

    kategorie = {kategorie.name: format_enum(kategorie.name) for kategorie in Kategorie}
    return jsonify(kategorie), 200

@ticket_bp.route('/getTicketStatus', methods=['GET'])
def get_ticket_status():
    def format_enum(enum_value):
        return enum_value.replace("_", " ").title()

    status = {status.name: format_enum(status.name) for status in TicketStatus}
    return jsonify(status), 200

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

def to_uuid(val):
    """Convert a value to UUID if it's not already a UUID."""
    return val if isinstance(val, uuid.UUID) else uuid.UUID(val)

@ticket_bp.route('/updateTicket', methods=['POST'])
def update_ticket():
    data = request.json
    try:
        ticket_id = to_uuid(data.get('ticket_id'))
        bearbeiter_id = to_uuid(data.get('bearbeiter_id'))
    except (ValueError, AttributeError):
        return jsonify({"message": "Ungültige Ticket- oder Bearbeiter-ID!"}), 400

    status = data.get('status')
    prioritaet = data.get('prioritaet')
    beschreibung = data.get('beschreibung')

    if not ticket_id or not status or not prioritaet:
        return jsonify({"message": "Fehlende Daten!"}), 400

    ticket = db.session.get(Ticket, ticket_id)
    if not ticket:
        return jsonify({"message": "Ticket nicht gefunden!"}), 404

    try:
        prioritaet_enum = Prioritaet(prioritaet)
        status_enum = TicketStatus(status)
    except ValueError:
        return jsonify({"message": "Ungültige Priorität oder Status!"}), 400

    historie = Historie(
        ticket_id=ticket_id,
        bearbeiter_id=bearbeiter_id,
        beschreibung=beschreibung,
        status=status_enum,
        geaendert_am=datetime.now(timezone.utc)
    )

    ticket.prioritaet = prioritaet_enum

    db.session.add(historie)
    db.session.commit()

    return jsonify({"message": "Ticket aktualisiert!"}), 200

@ticket_bp.route('/getKursTicketsByUser/<string:benutzer_id>', methods=['GET'])
def get_kurs_tickets_by_user(benutzer_id):
    kurse = Kurs.query.filter_by(kursleitung_id=benutzer_id).all()
    kurs_ids = [kurs.id for kurs in kurse]
    tickets = Ticket.query.filter(Ticket.kurs_id.in_(kurs_ids)).all()
    tickets = [ticket.serialize() for ticket in tickets]
    for ticket in tickets:
        ticket_status = Historie.query.filter_by(ticket_id=uuid.UUID(ticket['id'])).order_by(Historie.geaendert_am.desc()).first()
        ticket['status'] = ticket_status.status.value if ticket_status else 'Unbekannt'
    return jsonify(tickets), 200

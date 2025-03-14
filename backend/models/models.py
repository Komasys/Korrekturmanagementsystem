import uuid
from datetime import datetime
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class KategorieHaupt(Enum):
    FEHLER = "fehler"
    VERBESSERUNGSVORSCHLAG = "verbesserungsvorschlag"

class KategorieUnter(Enum):
    TIPPFEHLER = "tippfehler"
    INHALTLICHER_FEHLER = "inhaltlicher_fehler"
    FORMATIERUNGSFEHLER = "formatierungsfehler"
    ERWEITERUNG = "erweiterung"
    STRUKTURVERBESSERUNG = "sturkturverbesserung"

class Prioritaet(Enum):
    NIEDRIG = "niedrig"
    MITTEL = "mittel"
    HOCH = "hoch"

class Rolle(Enum):
    STUDENT = "student"
    TUTOR = "tutor"
    DOZENT = "dozent"
    QM = "qm"
    ADMIN = "admin"

class LernmaterialTyp(Enum):
    PDF = "pdf"
    VIDEO = "video"
    PRAESENTATION = "praesentation"
    QUIZ = "quiz"

class TicketStatus(Enum):
    NEU = "neu"
    ABGELEHNT = "abgelehnt"
    PRUEFUNG = "prüfung"
    ANPASSUNG = "anpassung"
    GESCHLOSSEN = "geschlossen"

class Benutzer(db.Model):
    __tablename__ = 'benutzer'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    rolle = db.Column(db.Enum(Rolle), nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    letzte_anmeldung = db.Column(db.TIMESTAMP, server_default=db.func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    beschreibung = db.Column(db.Text, nullable=False)
    kategorie_haupt = db.Column(db.Enum(KategorieHaupt), nullable=False)
    kategorie_unter = db.Column(db.Enum(KategorieUnter))
    erstelldatum = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    prioritaet = db.Column(db.Enum(Prioritaet))
    kurs_id = db.Column(UUID(as_uuid=True), db.ForeignKey('kurs.id'), nullable=False)
    ersteller_id = db.Column(UUID(as_uuid=True), db.ForeignKey('benutzer.id'), nullable=False)

class Lernmaterial(db.Model):
    __tablename__ = 'lernmaterial'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titel = db.Column(db.String(255), nullable=False)
    typ = db.Column(db.Enum(LernmaterialTyp), nullable=False)
    kurs_id = db.Column(UUID(as_uuid=True), db.ForeignKey('kurs.id'), nullable=False)
    erstelldatum = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    letzter_aktualisierung = db.Column(db.DateTime, nullable=True)

class Historie(db.Model):
    __tablename__ = 'historie'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticket_id = db.Column(UUID(as_uuid=True), db.ForeignKey('ticket.id'), nullable=False)
    bearbeiter_id = db.Column(UUID(as_uuid=True), db.ForeignKey('benutzer.id'), nullable=False)
    beschreibung = db.Column(db.Text, nullable=False)
    geaendert_am = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Enum(TicketStatus), nullable=False)
    pruefer_id = db.Column(UUID(as_uuid=True), db.ForeignKey('benutzer.id'), nullable=True)

class Kommentar(db.Model):
    __tablename__ = 'kommentar'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    benutzer_id = db.Column(UUID(as_uuid=True), db.ForeignKey('benutzer.id'), nullable=False)
    ticket_id = db.Column(UUID(as_uuid=True), db.ForeignKey('ticket.id'), nullable=False)
    nachricht = db.Column(db.Text, nullable=False)
    erstelldatum = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Kurs(db.Model):
    __tablename__ = 'kurs'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    kuerzel = db.Column(db.String(50), unique=True, nullable=False)
    kursleitung_id = db.Column(UUID(as_uuid=True), db.ForeignKey('benutzer.id'), nullable=True)

class Anhang(db.Model):
    __tablename__ = 'anhang'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticket_id = db.Column(UUID(as_uuid=True), db.ForeignKey('ticket.id'), nullable=False)
    dateiname = db.Column(db.String(255), nullable=False)

from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from .enums import Kategorie, Prioritaet
from . import db

class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    beschreibung = db.Column(db.Text, nullable=False)
    kategorie = db.Column(db.Enum(Kategorie), nullable=False)
    erstelldatum = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    prioritaet = db.Column(db.Enum(Prioritaet))
    kurs_id = db.Column(UUID(as_uuid=True), db.ForeignKey('kurs.id'), nullable=False)
    ersteller_id = db.Column(UUID(as_uuid=True), db.ForeignKey('benutzer.id'), nullable=False)

    def serialize(self):
        return {
            'id': str(self.id),
            'beschreibung': self.beschreibung,
            'kategorie': self.kategorie.value,
            'erstelldatum': self.erstelldatum.isoformat(),
            'prioritaet': self.prioritaet.value if self.prioritaet else None,
            'kurs_id': str(self.kurs_id),
            'ersteller_id': str(self.ersteller_id)
        }
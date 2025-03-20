from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from .enums import TicketStatus
from . import db

class Historie(db.Model):
    __tablename__ = 'historie'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticket_id = db.Column(UUID(as_uuid=True), db.ForeignKey('ticket.id'), nullable=False)
    bearbeiter_id = db.Column(UUID(as_uuid=True), db.ForeignKey('benutzer.id'), nullable=True)
    beschreibung = db.Column(db.Text, nullable=False)
    geaendert_am = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Enum(TicketStatus), nullable=False)
    pruefer_id = db.Column(UUID(as_uuid=True), db.ForeignKey('benutzer.id'), nullable=True)

    def serialize(self):
        return {
            'id': str(self.id),
            'ticket_id': str(self.ticket_id),
            'bearbeiter_id': str(self.bearbeiter_id),
            'beschreibung': self.beschreibung,
            'geaendert_am': self.geaendert_am.isoformat(),
            'status': self.status.value,
            'pruefer_id': str(self.pruefer_id) if self.pruefer_id else None
        }
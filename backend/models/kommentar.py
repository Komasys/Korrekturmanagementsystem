from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from . import db

class Kommentar(db.Model):
    __tablename__ = 'kommentar'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    benutzer_id = db.Column(UUID(as_uuid=True), db.ForeignKey('benutzer.id'), nullable=False)
    ticket_id = db.Column(UUID(as_uuid=True), db.ForeignKey('ticket.id'), nullable=False)
    nachricht = db.Column(db.Text, nullable=False)
    erstelldatum = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def serialize(self):
        return {
            'id': str(self.id),
            'benutzer_id': str(self.benutzer_id),
            'ticket_id': str(self.ticket_id),
            'nachricht': self.nachricht,
            'erstelldatum': self.erstelldatum.isoformat()
        }
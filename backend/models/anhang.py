from sqlalchemy.dialects.postgresql import UUID
import uuid
from . import db

class Anhang(db.Model):
    __tablename__ = 'anhang'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticket_id = db.Column(UUID(as_uuid=True), db.ForeignKey('ticket.id'), nullable=False)
    dateiname = db.Column(db.String(255), nullable=False)

    def serialize(self):
        return {
            'id': str(self.id),
            'ticket_id': str(self.ticket_id),
            'dateiname': self.dateiname
        }
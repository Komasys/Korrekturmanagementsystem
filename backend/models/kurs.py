from sqlalchemy.dialects.postgresql import UUID
import uuid
from . import db

class Kurs(db.Model):
    __tablename__ = 'kurs'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    kuerzel = db.Column(db.String(50), unique=True, nullable=False)
    kursleitung_id = db.Column(UUID(as_uuid=True), db.ForeignKey('benutzer.id'), nullable=True)

    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'kuerzel': self.kuerzel,
            'kursleitung_id': str(self.kursleitung_id) if self.kursleitung_id else None
        }
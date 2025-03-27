from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone
from .enums import LernmaterialTyp
from . import db

class Lernmaterial(db.Model):
    __tablename__ = 'lernmaterial'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titel = db.Column(db.String(255), nullable=False)
    typ = db.Column(db.Enum(LernmaterialTyp), nullable=False)
    kurs_id = db.Column(UUID(as_uuid=True), db.ForeignKey('kurs.id'), nullable=False)
    erstelldatum = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    letzter_aktualisierung = db.Column(db.DateTime, nullable=True)

    def serialize(self):
        return {
            'id': str(self.id),
            'titel': self.titel,
            'typ': self.typ.value,
            'kurs_id': str(self.kurs_id),
            'erstelldatum': self.erstelldatum.isoformat(),
            'letzter_aktualisierung': self.letzter_aktualisierung.isoformat() if self.letzter_aktualisierung else None
        }
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .enums import Rolle
from . import db

class Benutzer(db.Model):
    __tablename__ = 'benutzer'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    rolle = db.Column(db.Enum(Rolle), nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    letzte_anmeldung = db.Column(db.TIMESTAMP, server_default=db.func.now())

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def serialize(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'email': self.email,
            'rolle': self.rolle.value,
            'letzte_anmeldung': self.letzte_anmeldung.isoformat()
        }
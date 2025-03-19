from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .benutzer import Benutzer
from .ticket import Ticket
from .lernmaterial import Lernmaterial
from .historie import Historie
from .kommentar import Kommentar
from .kurs import Kurs
from .anhang import Anhang
from .enums import Kategorie, Prioritaet, Rolle, LernmaterialTyp, TicketStatus
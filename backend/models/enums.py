from enum import Enum

class Kategorie(Enum):
    TIPPFEHLER = "tippfehler"
    INHALTLICHER_FEHLER = "inhaltlicher_fehler"
    FORMATIERUNGSFEHLER = "formatierungsfehler"
    ERWEITERUNG = "erweiterung"
    STRUKTURVERBESSERUNG = "strukturverbesserung"

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
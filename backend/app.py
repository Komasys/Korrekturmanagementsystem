from flask import Flask, send_from_directory
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Eigene Module
from config import Config
from models import db

# Blueprints
from routes.auth_bp import auth_bp
from routes.kurs_bp import kurs_bp
from routes.ticket_bp import ticket_bp
from routes.lernmaterial_bp import lernmaterial_bp
from routes.uploads_bp import uploads_bp

# Initialisierung der App
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

# Datenbank und Migrations-Setup
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Registrierung der Blueprints
blueprints = [
    (auth_bp, "/auth"),
    (kurs_bp, "/kurs"),
    (lernmaterial_bp, "/lernmaterial"),
    (ticket_bp, "/ticket"),
    (uploads_bp, ""),
]

for bp, prefix in blueprints:
    app.register_blueprint(bp, url_prefix=prefix)

if __name__ == "__main__":
    app.run(debug=True)

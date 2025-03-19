from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os

# Eigene Module
from config import Config
from models import db

# Blueprints
from routes.auth_bp import auth_bp
from routes.kurs_bp import kurs_bp
from routes.ticket_bp import ticket_bp
from routes.lernmaterial_bp import lernmaterial_bp
from routes.anhang_bp import anhang_bp
from routes.benutzer_bp import benutzer_bp
from routes.historie_bp import historie_bp
from routes.kommentar_bp import kommentar_bp

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
    (anhang_bp, "/anhang"),
    (auth_bp, "/auth"),
    (benutzer_bp, "/benutzer"),
    (historie_bp, "/historie"),
    (kommentar_bp, "/kommentar"),
    (kurs_bp, "/kurs"),
    (lernmaterial_bp, "/lernmaterial"),
    (ticket_bp, "/ticket"),
]

for bp, prefix in blueprints:
    app.register_blueprint(bp, url_prefix=prefix)

@app.before_request
def limit_remote_addr():
    allowed_ip = os.getenv("ALLOWED_IP", "127.0.0.1")  # Einzelne erlaubte IP
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)

    if client_ip != allowed_ip:
        return jsonify({"message": "Access denied"}), 403

if __name__ == "__main__":
    app.run(debug=True)

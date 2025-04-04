from flask import Blueprint, request, jsonify
from models import db, Benutzer, Rolle
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timezone
import logging

# Configure logging
logging.basicConfig(
    filename='login_logs.txt',  # Logdatei
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/signin', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Ungültige JSON-Daten!"}), 400

    user = Benutzer.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({"message":"Ungültige Anmeldedaten!"}), 401

    user.letzte_anmeldung = datetime.now(timezone.utc)
    db.session.commit()

    # Log the login
    logging.info(f"Benutzer-ID: {user.id}, Email: {user.email}, IP: {request.remote_addr}")

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

@auth_bp.route('/dashboard', methods=['POST'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = Benutzer.query.get(current_user_id)
    return jsonify(logged_in_as=user.name), 200

@auth_bp.route('/user-info', methods=['GET'])
@jwt_required()
def user_info():
    current_user_id = get_jwt_identity()
    user = Benutzer.query.get(current_user_id)
    if user:
        return jsonify({
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "rolle": user.rolle.value,
        }), 200

    return jsonify({"message": "Benutzer nicht gefunden"}), 400

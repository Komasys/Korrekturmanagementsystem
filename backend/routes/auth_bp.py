from flask import Blueprint, request, jsonify
from models import db, Benutzer, Rolle
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Ungültige JSON-Daten!"}), 400

    if Benutzer.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Benutzer existiert bereits!"}), 400

    new_user = Benutzer(
        name=data['name'],
        email=data['email'],
        password = data['password'],
        rolle=Rolle.STUDENT # Default role for new users is STUDENT (can be changed later by admin)
    )
    #new_user.password = data['password']

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Benutzer erfolgreich registriert!'}), 201

@auth_bp.route('/signin', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Ungültige JSON-Daten!"}), 400

    user = Benutzer.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({"message":"Ungültige Anmeldedaten!"}), 401

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
        }), 200

    return jsonify({"message": "Benutzer nicht gefunden"}), 400

from flask import Blueprint, request, jsonify
from models.models import Kurs
kurs_bp = Blueprint('kurs_bp', __name__)

@kurs_bp.route('/getKurse', methods=['GET'])
def get_kurse():
    kurse = Kurs.query.all()
    kurse_list = [{"id": kurs.id, "name": kurs.name, "kuerzel": kurs.kuerzel} for kurs in kurse]
    return jsonify(kurse_list), 200

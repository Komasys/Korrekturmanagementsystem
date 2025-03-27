from flask import Blueprint, jsonify
from models import Lernmaterial
from uuid import UUID

lernmaterial_bp = Blueprint('lernmaterial_bp', __name__)

@lernmaterial_bp.route('/getLernmaterial/<string:kurs_id>', methods=['GET'])
def get_lernmaterial(kurs_id):
    try:
        kurs_uuid = UUID(kurs_id)  # 🛠️ Konvertiere zu UUID-Objekt
    except ValueError:
        return jsonify({"error": "Ungültige UUID"}), 400

    lernmaterialien = Lernmaterial.query.filter_by(kurs_id=kurs_uuid).all()
    lernmaterialien_list = [lm.serialize() for lm in lernmaterialien]
    return jsonify(lernmaterialien_list), 200

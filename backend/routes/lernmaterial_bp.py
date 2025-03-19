from flask import Blueprint, jsonify
from models import Lernmaterial

lernmaterial_bp = Blueprint('lernmaterial_bp', __name__)

@lernmaterial_bp.route('/getLernmaterial/<string:kurs_id>', methods=['GET'])
def get_lernmaterial(kurs_id):
    lernmaterialien = Lernmaterial.query.filter_by(kurs_id=kurs_id).all()
    lernmaterialien_list = [lm.serialize() for lm in lernmaterialien]
    return jsonify(lernmaterialien_list), 200
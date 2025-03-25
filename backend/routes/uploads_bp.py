from flask import Blueprint, send_from_directory

uploads_bp = Blueprint('uploads_bp', __name__)

@uploads_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

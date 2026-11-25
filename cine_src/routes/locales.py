from flask import Blueprint, jsonify
from repositories import locales as repositories

locales_bp = Blueprint('locales_bp', __name__)

@locales_bp.route('/locales', methods=['GET'])
def get_locales():
    try:
        locales = repositories.listar_locales()
        return jsonify(locales), 200
    except Exception as e:
        print("\n---> ERROR DE MYSQL:", str(e), "\n")
        return jsonify({"error": str(e)}), 500
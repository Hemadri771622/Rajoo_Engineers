from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.db_service import get_updates

telemetry_bp = Blueprint("telemetry", __name__, url_prefix="/api/telemetry")

@telemetry_bp.route("", methods=["GET"])
@jwt_required()
def telemetry_all_tables():
    role = get_jwt_identity()
    data = get_updates()

    return jsonify({
        "role": role,
        "data": data
    })

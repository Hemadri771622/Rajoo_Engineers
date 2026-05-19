from flask import Blueprint, jsonify, current_app

health_bp = Blueprint("health", __name__)

@health_bp.route("/")
def home():
    return jsonify({
        "status": "running",
        "database": current_app.config["DB_FILE"],
        "message": "Flask IoT backend running successfully."
    })

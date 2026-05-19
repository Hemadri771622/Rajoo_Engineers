from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

USERS = {
    "Operator": "1234",
    "Admin": "admin123",
    "Guest": "guest123"
}

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    role = data.get("role")
    password = data.get("password")

    if role in USERS and USERS[role] == password:
        token = create_access_token(identity=role)
        return jsonify(access_token=token, role=role)

    return jsonify({"message": "Invalid credentials"}, 401)

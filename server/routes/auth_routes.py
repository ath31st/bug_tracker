from flask import Blueprint, request, jsonify
from services import AuthService


def create_auth_routes(auth_service: AuthService):
    auth_routes = Blueprint("auth_routes", __name__, url_prefix="/api/v1/auth")

    @auth_routes.route("/login", methods=["POST"])
    def login():
        try:
            data = request.get_json()
            username = data["username"]
            password = data["password"]
            response = auth_service.login(username, password)
            return jsonify(response), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 401

    return auth_routes

from flask import Blueprint, request, jsonify
from services import UserService
from flask_bcrypt import Bcrypt
from dto import UserSchema, NewUserSchema
from marshmallow import ValidationError


def create_user_routes(bcrypt: Bcrypt):
    user_routes = Blueprint("user_routes", __name__, url_prefix="/api/v1/users")
    user_service = UserService(bcrypt)
    user_schema = UserSchema()
    new_user_schema = NewUserSchema()

    @user_routes.before_request
    def check_json_content_type():
        if request.method in ["POST", "PUT"]:
            if request.content_type != "application/json":
                return (
                    jsonify({"error": "Content-Type must be 'application/json'"}),
                    415,
                )
            if request.get_json(silent=True) is None:
                return jsonify({"error": "Invalid or missing JSON body"}), 400

    @user_routes.route("/", methods=["GET"])
    def get_all_users():
        try:
            users = user_service.get_all_users()
            return jsonify(user_schema.dump(users, many=True)), 200
        except Exception as e:
            return jsonify({"error": "Internal Server Error"}), 500

    @user_routes.route("/<int:user_id>", methods=["GET"])
    def get_user(user_id):
        try:
            user = user_service.get_user_by_id(user_id)
            return jsonify(user_schema.dump(user)), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": "Internal Server Error"}), 500

    @user_routes.route("/", methods=["POST"])
    def create_user():
        try:
            data = request.get_json()
            user_data = new_user_schema.load(data)

            user = user_service.create_user(**user_data)
            return jsonify(user_schema.dump(user)), 201
        except (ValueError, ValidationError) as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal Server Error: " + str(e)}), 500

    @user_routes.route("/<int:user_id>", methods=["PUT"])
    def update_user(user_id):
        try:
            data = request.get_json()
            update_data = new_user_schema.load(data, partial=True)

            user = user_service.update_user(user_id, **update_data)
            return jsonify(user_schema.dump(user)), 200
        except (ValueError, ValidationError) as e:
            return (
                jsonify({"error": str(e)}),
                400,
            )
        except Exception as e:
            return jsonify({"error": "Internal Server Error" + str(e)}), 500

    @user_routes.route("/<int:user_id>", methods=["DELETE"])
    def delete_user(user_id):
        try:
            user_service.delete_user(user_id)
            return "", 204
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": "Internal Server Error"}), 500

    return user_routes

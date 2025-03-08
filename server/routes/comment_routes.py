from flask import Blueprint, request, jsonify
from services import CommentService
from validations.comment import CommentSchema, NewCommentSchema
from marshmallow import ValidationError


def create_comment_routes(comment_service: CommentService):
    comment_routes = Blueprint(
        "comment_routes", __name__, url_prefix="/api/v1/comments"
    )
    comment_service = comment_service
    comment_schema = CommentSchema()
    new_comment_schema = NewCommentSchema()

    @comment_routes.before_request
    def check_json_content_type():
        if request.method in ["POST", "PUT"]:
            if request.content_type != "application/json":
                return (
                    jsonify({"error": "Content-Type must be 'application/json'"}),
                    415,
                )
            if request.get_json(silent=True) is None:
                return jsonify({"error": "Invalid or missing JSON body"}), 400

    @comment_routes.route("/", methods=["POST"])
    def create_comment():
        try:
            data = request.get_json()
            comment_data = new_comment_schema.load(data)

            comment = comment_service.create_comment(**comment_data)
            return jsonify(comment_schema.dump(comment)), 201
        except (ValueError, ValidationError) as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal Server Error: " + str(e)}), 500

    @comment_routes.route("/<int:comment_id>", methods=["GET"])
    def get_comment(comment_id):
        try:
            comment = comment_service.get_comment_by_id(comment_id)
            return jsonify(comment_schema.dump(comment)), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": "Internal Server Error"}), 500

    @comment_routes.route("/", methods=["GET"])
    def get_all_comments():
        try:
            comments = comment_service.get_all_comments()
            return jsonify(comment_schema.dump(comments, many=True)), 200
        except Exception as e:
            return jsonify({"error": "Internal Server Error"}), 500

    @comment_routes.route("/<int:comment_id>", methods=["PUT"])
    def update_comment(comment_id):
        try:
            data = request.get_json()
            comment_data = new_comment_schema.load(data, partial=True)

            comment = comment_service.update_comment(comment_id, **comment_data)
            return jsonify(comment_schema.dump(comment)), 200
        except (ValueError, ValidationError) as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal Server Error: " + str(e)}), 500

    @comment_routes.route("/<int:comment_id>", methods=["DELETE"])
    def delete_comment(comment_id):
        try:
            comment_service.delete_comment(comment_id)
            return "", 204
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": "Internal Server Error"}), 500

    return comment_routes

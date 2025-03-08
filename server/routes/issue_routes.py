from flask import Blueprint, request, jsonify
from services import IssueService
from validations.issue import IssueSchema, NewIssueSchema
from marshmallow import ValidationError


def create_issue_routes():
    issue_routes = Blueprint("issue_routes", __name__, url_prefix="/api/v1/issues")
    issue_service = IssueService()
    issue_schema = IssueSchema()
    new_issue_schema = NewIssueSchema()

    @issue_routes.route("/", methods=["POST"])
    def create_issue():
        try:
            data = request.get_json()
            issue_data = new_issue_schema.load(data)

            issue = issue_service.create_issue(**issue_data)
            return jsonify(issue_schema.dump(issue)), 201
        except (ValueError, ValidationError) as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal Server Error: " + str(e)}), 500

    @issue_routes.route("/", methods=["GET"])
    def get_all_issues():
        try:
            issues = issue_service.get_all_issues()
            return jsonify(issue_schema.dump(issues, many=True)), 200
        except Exception as e:
            return jsonify({"error": "Internal Server Error"}), 500

    @issue_routes.route("/<int:issue_id>", methods=["GET"])
    def get_issue(issue_id):
        try:
            issue = issue_service.get_issue_by_id(issue_id)
            return jsonify(issue_schema.dump(issue)), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": "Internal Server Error"}), 500

    @issue_routes.route("/<int:issue_id>", methods=["PUT"])
    def update_issue(issue_id):
        try:
            data = request.get_json()
            update_data = new_issue_schema.load(data, partial=True)

            issue = issue_service.update_issue(issue_id, **update_data)
            return jsonify(issue_schema.dump(issue)), 200
        except (ValueError, ValidationError) as e:
            return (
                jsonify({"error": str(e)}),
                400,
            )
        except Exception as e:
            return jsonify({"error": "Internal Server Error" + str(e)}), 500

    @issue_routes.route("/<int:issue_id>", methods=["DELETE"])
    def delete_issue(issue_id):
        try:
            issue_service.delete_issue(issue_id)
            return "", 204
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": "Internal Server Error"}), 500

    return issue_routes

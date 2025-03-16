from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from dto import Page
from exceptions import IssueServiceException
from services import IssueService
from validations.issue import IssueSchema, NewIssueSchema, FullIssueSchema
from marshmallow import ValidationError


def create_issue_routes(issue_service: IssueService):
    issue_routes = Blueprint("issue_routes", __name__, url_prefix="/api/v1/issues")
    issue_schema = IssueSchema()
    full_issue_schema = FullIssueSchema()
    new_issue_schema = NewIssueSchema()

    @issue_routes.before_request
    @jwt_required()
    def protect_all_routes():
        pass

    @issue_routes.before_request
    def check_json_content_type():
        if request.method in ["POST", "PUT"]:
            if request.content_type != "application/json":
                return (
                    jsonify({"error": "Content-Type must be 'application/json'"}),
                    415,
                )
            if request.get_json(silent=True) is None:
                return jsonify({"error": "Invalid or missing JSON body"}), 400

    @issue_routes.route("/", methods=["POST"])
    def create_issue():
        try:
            current_user_id = int(get_jwt_identity())
            data = request.get_json()
            issue_data = new_issue_schema.load(data)
            issue_data["reporter_id"] = current_user_id

            issue = issue_service.create_issue(**issue_data)
            return jsonify(issue_schema.dump(issue)), 201
        except (ValueError, ValidationError, IssueServiceException) as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal Server Error: " + str(e)}), 500

    @issue_routes.route("/", methods=["GET"])
    def get_all_issues():
        try:
            page = request.args.get("page", 1, type=int)
            per_page = request.args.get("elementsPerPage", 10, type=int)

            pageIssues = issue_service.get_all_issues_paginated(page, per_page)

            return jsonify(pageIssues.to_dict(issue_schema)), 200
        except Exception as e:
            return jsonify({"error": "Internal Server Error"}), 500

    @issue_routes.route("/<int:issue_id>", methods=["GET"])
    def get_issue(issue_id):
        try:
            issue = issue_service.get_issue_by_id(issue_id)
            return jsonify(full_issue_schema.dump(issue)), 200
        except IssueServiceException as e:
            return jsonify({"error": str(e)}), 400
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
        except (ValueError, ValidationError, IssueServiceException) as e:
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
        except IssueServiceException as e:
            return jsonify({"error": str(e)}), 400
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": "Internal Server Error"}), 500

    @issue_routes.route("/<int:issue_id>/assign", methods=["PATCH"])
    def assign_issue(issue_id):
        try:
            current_user_id = int(get_jwt_identity())
            updated_issue = issue_service.assign_issue(issue_id, current_user_id)
            return jsonify(full_issue_schema.dump(updated_issue)), 200
        except IssueServiceException as e:
            return jsonify({"error": str(e)}), 400
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            return jsonify({"error": "Internal Server Error"}), 500

    return issue_routes

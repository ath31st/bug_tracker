from flask import jsonify
from humps import camelize
from .user_routes import create_user_routes
from .issue_routes import create_issue_routes
from .comment_routes import create_comment_routes
from .auth_routes import create_auth_routes
from flask_bcrypt import Bcrypt


def register_routes(
    app, bcrypt: Bcrypt, user_service, comment_service, issue_service, auth_service
):

    @app.after_request
    def camelize_response(response):
        if response.content_type == "application/json":
            data = response.get_json()
            if data is not None:
                response.set_data(jsonify(camelize(data)).data)
        return response

    app.register_blueprint(create_user_routes(bcrypt, user_service))
    app.register_blueprint(create_issue_routes(issue_service))
    app.register_blueprint(create_comment_routes(comment_service, issue_service))
    app.register_blueprint(create_auth_routes(auth_service))

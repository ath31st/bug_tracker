from flask import Flask
from config.config import Config
from models import db
from repositories import UserRepository, CommentRepository, IssueRepository
from services import jwt
from flask_bcrypt import Bcrypt
from routes import register_routes
from services import UserService, CommentService, IssueService, AuthService
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    jwt.init_app(app)
    db.init_app(app)
    bcrypt = Bcrypt(app)

    user_repository = UserRepository(db)
    comment_repository = CommentRepository(db)
    issue_repository = IssueRepository(db)

    user_service = UserService(bcrypt, user_repository)
    comment_service = CommentService(comment_repository)
    issue_service = IssueService(issue_repository)
    auth_service = AuthService(user_service)

    register_routes(
        app, bcrypt, user_service, comment_service, issue_service, auth_service
    )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

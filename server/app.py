from flask import Flask
from config.config import Config
from models import db
from repositories import UserRepository, CommentRepository, IssueRepository
from services import jwt
from flask_bcrypt import Bcrypt
from routes import register_routes
from services import UserService, CommentService, IssueService, AuthService


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt.init_app(app)
    db.init_app(app)
    bcrypt = Bcrypt(app)

    user_repository = UserRepository(db)
    comment_repository = CommentRepository(db)
    issue_repository = IssueRepository(db)

    user_service = UserService(bcrypt, user_repository)
    comment_service = CommentService(comment_repository)
    issue_service = IssueService(issue_repository)
    auth_service = AuthService(user_repository)

    register_routes(
        app, bcrypt, user_service, comment_service, issue_service, auth_service
    )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)

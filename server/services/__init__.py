from .user_service import UserService
from .comment_service import CommentService
from .issue_service import IssueService
from .auth_service import AuthService
from flask_jwt_extended import JWTManager

jwt = JWTManager()

__all__ = ["jwt", "UserService", "CommentService", "IssueService", "AuthService"]

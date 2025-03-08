from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from repositories import UserRepository
from exceptions import UnauthorizedException


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def login(self, username: str, password: str) -> dict:
        user = self.user_repository.find_by_username(username)
        if not user or not check_password_hash(user.password_hash, password):
            raise UnauthorizedException("Invalid username or password")

        access_token = create_access_token(
            identity=user.id, additional_claims={"username": user.username}
        )
        return {"access_token": access_token}

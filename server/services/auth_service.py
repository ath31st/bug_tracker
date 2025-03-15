from typing import Optional
from flask_jwt_extended import create_access_token
from services import UserService
from exceptions import UnauthorizedException


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def login(self, username: str, password: str) -> dict:
        user = self.user_service.get_user_by_username(username)
        if not user or not self.user_service.check_password(username, str(password)):
            raise UnauthorizedException("Invalid username or password")

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"username": user.username, "id": user.id},
        )
        return {"access_token": access_token}

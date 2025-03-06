from repositories import UserRepository
from flask_bcrypt import Bcrypt
from typing import Optional, List
from models.user import User


class UserService:
    def __init__(self, bcrypt: Bcrypt):
        self.repository = UserRepository()
        self.bcrypt = bcrypt

    def create_user(self, username: str, email: str, password: str) -> User:
        if not username or not email or not password:
            raise ValueError("Username, email, and password are required")

        hashed_password = self.bcrypt.generate_password_hash(password).decode("utf-8")
        return self.repository.create(username, email, hashed_password)

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        user = self.repository.find_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        return user

    def get_user_by_username(self, username: str) -> Optional[User]:
        user = self.repository.find_by_username(username)
        if not user:
            raise ValueError(f"User with username {username} not found")
        return user

    def get_all_users(self) -> List[User]:
        users = self.repository.get_all()
        if not users:
            return []
        return users

    def update_user(
        self,
        user_id: int,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
    ) -> User:
        user = self.repository.find_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        if password:
            password = self.bcrypt.generate_password_hash(password).decode("utf-8")

        updated_user = self.repository.update(user_id, username, email, password)
        if not updated_user:
            raise ValueError("Failed to update user")
        return updated_user

    def delete_user(self, user_id: int) -> None:
        if not self.repository.delete(user_id):
            raise ValueError(
                f"User with ID {user_id} not found or could not be deleted"
            )

    def check_password(self, username: str, password: str) -> bool:
        user = self.repository.find_by_username(username)
        if not user:
            return False
        return self.bcrypt.check_password_hash(user.password, password)

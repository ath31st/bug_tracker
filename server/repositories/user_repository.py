from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from models import User
from typing import Optional


class UserRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create(self, username: str, email: str, password: str) -> User:
        user = User(username=username, email=email, password=password)
        self.db.session.add(user)
        self.db.session.commit()
        return user

    def find_by_id(self, user_id: int) -> Optional[User]:
        return self.db.session.get(User, user_id)

    def find_by_username(self, username: str) -> Optional[User]:
        return (
            self.db.session.query(User)
            .filter(func.lower(User.username) == username.lower())
            .first()
        )

    def get_all(self) -> list[User]:
        return self.db.session.query(User).all()

    def update(
        self,
        user_id: int,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
    ) -> Optional[User]:
        user = self.db.session.get(User, user_id)
        if not user:
            return None
        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.password = password
        self.db.session.commit()
        return user

    def delete(self, user_id: int) -> bool:
        user = self.db.session.get(User, user_id)
        if not user:
            return False
        self.db.session.delete(user)
        self.db.session.commit()
        return True

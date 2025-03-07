from models import db, User
from typing import List, Optional


class UserRepository:
    @staticmethod
    def create(username: str, email: str, password: str) -> User:
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def find_by_id(user_id: int) -> Optional[User]:
        return User.query.get(user_id)

    @staticmethod
    def find_by_username(username: str) -> Optional[User]:
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_all() -> List[User]:
        return User.query.all()

    @staticmethod
    def update(
        user_id: int,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
    ) -> Optional[User]:
        user = User.query.get(user_id)
        if not user:
            return None
        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.password = password
        db.session.commit()
        return user

    @staticmethod
    def delete(user_id: int) -> bool:
        user = User.query.get(user_id)
        if not user:
            return False
        db.session.delete(user)
        db.session.commit()
        return True

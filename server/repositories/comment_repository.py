from flask_sqlalchemy import SQLAlchemy
from models import Comment
from typing import Optional


class CommentRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create(self, content: str, issue_id: int, author_id: int) -> Comment:
        comment = Comment(content=content, issue_id=issue_id, author_id=author_id)
        self.db.session.add(comment)
        self.db.session.commit()
        return comment

    def get_all(self) -> list[Comment]:
        return self.db.session.query(Comment).all()

    def find_by_id(self, comment_id: int) -> Optional[Comment]:
        return self.db.session.get(Comment, comment_id)

    def update(self, comment_id: int, content: str) -> Optional[Comment]:
        comment = self.db.session.get(Comment, comment_id)
        if not comment:
            return None
        comment.content = content
        self.db.session.commit()
        return comment

    def find_by_issue_id(self, issue_id: int) -> list[Comment]:
        return self.db.session.query(Comment).filter_by(issue_id=issue_id).all()

    def delete(self, comment_id: int) -> bool:
        comment = self.db.session.get(Comment, comment_id)
        if not comment:
            return False
        self.db.session.delete(comment)
        self.db.session.commit()
        return True

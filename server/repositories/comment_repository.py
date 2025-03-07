from models import db, Comment
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List, Optional


class CommentRepository:
    @staticmethod
    def create(content: str, issue_id: int, author_id: int) -> Comment:
        comment = Comment(content=content, issue_id=issue_id, author_id=author_id)
        db.session.add(comment)
        db.session.commit()
        return comment

    @staticmethod
    def get_all() -> List[Comment]:
        return Comment.query.all()

    @staticmethod
    def find_by_id(comment_id: int) -> Optional[Comment]:
        return Comment.query.get(comment_id)

    @staticmethod
    def update(comment_id: int, content: str) -> Optional[Comment]:
        comment = Comment.query.get(comment_id)
        if not comment:
            return None
        comment.content = content
        db.session.commit()
        return comment

    @staticmethod
    def find_by_issue_id(issue_id: int) -> List[Comment]:
        return Comment.query.filter_by(issue_id=issue_id).all()

    @staticmethod
    def delete(comment_id: int) -> bool:
        comment = Comment.query.get(comment_id)
        if not comment:
            return False
        db.session.delete(comment)
        db.session.commit()
        return True

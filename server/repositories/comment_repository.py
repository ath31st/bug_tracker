from models import db, Comment
from sqlalchemy.exc import IntegrityError
from typing import List, Optional


class CommentRepository:
    @staticmethod
    def create(self, content: str, issue_id: int, author_id: int) -> Comment:
        comment = Comment(content=content, issue_id=issue_id, author_id=author_id)
        db.session.add(comment)
        db.session.commit()
        return comment

    @staticmethod
    def get_all(self) -> List[Comment]:
        return Comment.query.all()

    @staticmethod
    def find_by_id(self, comment_id: int) -> Optional[Comment]:
        return Comment.query.get(comment_id)

    @staticmethod
    def update(self, comment_id: int, content: str) -> Comment:
        comment = Comment.query.get(comment_id)
        if not comment:
            raise ValueError("Comment not found")
        comment.content = content
        db.session.commit()
        return comment

    @staticmethod
    def find_by_issue_id(self, issue_id: int) -> List[Comment]:
        return Comment.query.filter_by(issue_id=issue_id).all()

    @staticmethod
    def delete(self, comment_id: int) -> bool:
        comment = Comment.query.get(comment_id)
        if not comment:
            return False
        db.session.delete(comment)
        db.session.commit()
        return True

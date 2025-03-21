from repositories import CommentRepository
from typing import Optional
from models import Comment
from sqlalchemy.exc import IntegrityError


class CommentService:
    def __init__(self, comment_repository: CommentRepository):
        self.repository = comment_repository

    def create_comment(self, content: str, issue_id: int, author_id: int) -> Comment:
        if not content or not issue_id or not author_id:
            raise ValueError("Content, issue ID, and author ID are required")

        try:
            comment = self.repository.create(content, issue_id, author_id)
            return comment
        except IntegrityError:
            raise ValueError("Comment creation failed due to integrity constraint")
        except Exception as e:
            raise ValueError(f"Comment creation failed: {str(e)}")

    def get_comment_by_id(self, comment_id: int) -> Optional[Comment]:
        comment = self.repository.find_by_id(comment_id)
        if not comment:
            raise ValueError(f"Comment with ID {comment_id} not found")
        return comment

    def update_comment(self, comment_id: int, editor_id: int, content: str) -> Comment:
        if not content:
            raise ValueError("Comment content is required")

        if not self.check_if_comment_exists(comment_id):
            raise ValueError(f"Comment with ID {comment_id} not found")

        if not self.check_if_user_is_author(comment_id, editor_id):
            raise ValueError("Only the author of the comment can update it")

        try:
            updated_comment = self.repository.update(comment_id, content)
            if not updated_comment:
                raise ValueError(f"Comment with ID {comment_id} not found")
            return updated_comment
        except IntegrityError:
            raise ValueError("Comment update failed due to integrity constraint")
        except Exception as e:
            raise ValueError(f"Comment update failed: {str(e)}")

    def get_comments_by_issue_id(self, issue_id: int) -> list[Comment]:
        return self.repository.find_by_issue_id(issue_id) or []

    def delete_comment(self, comment_id: int, author_id: int) -> None:
        try:
            if not self.check_if_user_is_author(comment_id, author_id):
                raise ValueError("Only the author of the comment can delete it")

            if not self.repository.delete(comment_id):
                raise ValueError(
                    f"Comment with ID {comment_id} not found or could not be deleted"
                )
        except Exception as e:
            raise ValueError(f"Comment deletion failed: {str(e)}")

    def check_if_comment_exists(self, comment_id: int) -> bool:
        return self.repository.check_if_comment_exists(comment_id)

    def check_if_user_is_author(self, comment_id: int, user_id: int) -> bool:
        return self.repository.check_if_user_is_author(comment_id, user_id)

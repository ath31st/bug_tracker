from typing import List, Optional
from models import db, Issue
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


class IssueRepository:
    @staticmethod
    def create(self, title: str, description: Optional[str], reporter_id: int) -> Issue:
        issue = Issue(
            title=title,
            description=description,
            reporter_id=reporter_id,
        )
        try:
            db.session.add(issue)
            db.session.commit()
            return issue
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Issue creation failed due to integrity constraint")
        except SQLAlchemyError:
            db.session.rollback()
            raise ValueError("Issue creation failed")

    @staticmethod
    def find_by_id(self, issue_id: int) -> Issue:
        return Issue.query.get(issue_id)

    @staticmethod
    def get_all(self) -> List[Issue]:
        return Issue.query.all()

    @staticmethod
    def get_by_reporter_id(self, reporter_id: int) -> List[Issue]:
        return Issue.query.filter_by(reporter_id=reporter_id).all()

    @staticmethod
    def get_by_assignee_id(self, assignee_id: int) -> List[Issue]:
        return Issue.query.filter_by(assignee_id=assignee_id).all()

    @staticmethod
    def update(
        self,
        issue_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        assignee_id: Optional[int] = None,
    ) -> Issue:
        issue = Issue.query.get(issue_id)
        if not issue:
            raise ValueError("Issue not found")
        if title:
            issue.title = title
        if description:
            issue.description = description
        if status:
            issue.status = status
        if priority:
            issue.priority = priority
        if assignee_id:
            issue.assignee_id = assignee_id
        try:
            db.session.commit()
            return issue
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Issue update failed due to integrity constraint")
        except SQLAlchemyError:
            db.session.rollback()
            raise ValueError("Issue update failed")

    @staticmethod
    def delete(self, issue_id: int) -> bool:
        issue = Issue.query.get(issue_id)
        if not issue:
            return False
        try:
            db.session.delete(issue)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return False

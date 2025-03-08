from typing import List, Optional
from models import Issue, Priority, IssueStatus
from flask_sqlalchemy import SQLAlchemy


class IssueRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create(
        self,
        title: str,
        description: Optional[str],
        status: IssueStatus,
        priority: Priority,
        reporter_id: int,
    ) -> Issue:
        issue = Issue(
            title=title,
            description=description,
            status=status,
            priority=priority,
            reporter_id=reporter_id,
        )
        self.db.session.add(issue)
        self.db.session.commit()
        return issue

    def find_by_id(self, issue_id: int) -> Optional[Issue]:
        return self.db.session.get(Issue, issue_id)

    def get_all(self) -> List[Issue]:
        return self.db.session.query(Issue).all()

    def get_by_reporter_id(self, reporter_id: int) -> List[Issue]:
        return self.db.session.query(Issue).filter_by(reporter_id=reporter_id).all()

    def get_by_assignee_id(self, assignee_id: int) -> List[Issue]:
        return self.db.session.query(Issue).filter_by(assignee_id=assignee_id).all()

    def update(
        self,
        issue_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[IssueStatus] = None,
        priority: Optional[Priority] = None,
        assignee_id: Optional[int] = None,
    ) -> Optional[Issue]:
        issue = self.db.session.get(Issue, issue_id)
        if not issue:
            return None
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
        self.db.session.commit()
        return issue

    def delete(self, issue_id: int) -> bool:
        issue = self.db.session.get(Issue, issue_id)
        if not issue:
            return False
        self.db.session.delete(issue)
        self.db.session.commit()
        return True

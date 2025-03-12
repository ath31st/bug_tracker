from typing import Optional
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

    def get_all(self) -> list[Issue]:
        return self.db.session.query(Issue).all()

    def get_all_paginated(self, page: int = 1, per_page: int = 10) -> list[Issue]:
        return (
            self.db.session.query(Issue)
            .order_by(Issue.id)
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

    def get_by_reporter_id(
        self, reporter_id: int, page: int = 1, per_page: int = 10
    ) -> list[Issue]:
        return (
            self.db.session.query(Issue)
            .filter_by(reporter_id=reporter_id)
            .order_by(Issue.id)
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

    def get_by_assignee_id(
        self, assignee_id: int, page: int = 1, per_page: int = 10
    ) -> list[Issue]:
        return (
            self.db.session.query(Issue)
            .filter_by(assignee_id=assignee_id)
            .order_by(Issue.id)
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

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

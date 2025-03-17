from typing import Optional

from sqlalchemy import exists, or_, select, asc, desc
from models import Issue, Priority, IssueStatus, Comment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload, subqueryload


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
        return (
            self.db.session.query(Issue)
            .options(
                joinedload(Issue.reporter),
                joinedload(Issue.assignee),
                subqueryload(Issue.comments).joinedload(Comment.author),
            )
            .get(issue_id)
        )

    def get_all(self) -> list[Issue]:
        return self.db.session.query(Issue).all()

    def get_all_paginated(
        self,
        page: int = 1,
        per_page: int = 10,
        sort_key: str = "id",
        sort_direction: str = "asc",
    ) -> list[Issue]:
        query = self.db.session.query(Issue).options(
            joinedload(Issue.reporter),
            joinedload(Issue.assignee),
        )

        direction = asc if sort_direction == "asc" else desc
        sort_column = getattr(Issue, sort_key, Issue.id)

        query = query.order_by(direction(sort_column))

        query = query.offset((page - 1) * per_page).limit(per_page)
        return query.all()

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

    def assign_issue(
        self, issue_id: int, assignee_id: int, status: IssueStatus
    ) -> Optional[Issue]:
        issue = self.db.session.get(Issue, issue_id)
        if not issue:
            return None
        issue.assignee_id = assignee_id
        issue.status = status
        self.db.session.commit()
        return issue

    def check_if_issue_exists_and_not_closed(self, issue_id: int) -> bool:
        query = select(
            exists().where(Issue.id == issue_id, Issue.status != IssueStatus.CLOSED)
        )
        return self.db.session.execute(query).scalar()

    def check_if_issue_assigned(self, issue_id: int) -> bool:
        query = select(exists().where(Issue.id == issue_id, Issue.assignee_id != None))
        return self.db.session.execute(query).scalar()

    def check_if_user_is_assignee_or_reporter_of_issue(
        self, issue_id: int, user_id: int
    ) -> bool:
        query = select(
            exists().where(
                Issue.id == issue_id,
                or_(
                    Issue.assignee_id == user_id,
                    Issue.reporter_id == user_id,
                ),
            )
        )
        return self.db.session.execute(query).scalar()

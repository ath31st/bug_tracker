from typing import List, Optional
from models import db, Issue, Priority, IssueStatus


class IssueRepository:
    @staticmethod
    def create(
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
        db.session.add(issue)
        db.session.commit()
        return issue

    @staticmethod
    def find_by_id(issue_id: int) -> Optional[Issue]:
        return Issue.query.get(issue_id)

    @staticmethod
    def get_all() -> List[Issue]:
        return Issue.query.all()

    @staticmethod
    def get_by_reporter_id(reporter_id: int) -> List[Issue]:
        return Issue.query.filter_by(reporter_id=reporter_id).all()

    @staticmethod
    def get_by_assignee_id(assignee_id: int) -> List[Issue]:
        return Issue.query.filter_by(assignee_id=assignee_id).all()

    @staticmethod
    def update(
        issue_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[IssueStatus] = None,
        priority: Optional[Priority] = None,
        assignee_id: Optional[int] = None,
    ) -> Optional[Issue]:
        issue = Issue.query.get(issue_id)
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
        db.session.commit()
        return issue

    @staticmethod
    def delete(issue_id: int) -> bool:
        issue = Issue.query.get(issue_id)
        if not issue:
            return False
        db.session.delete(issue)
        db.session.commit()
        return True

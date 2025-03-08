from repositories import IssueRepository
from typing import List, Optional
from models import Issue, IssueStatus, Priority
from sqlalchemy.exc import IntegrityError


class IssueService:
    def __init__(self, issue_repository: IssueRepository):
        self.repository = issue_repository

    def create_issue(
        self,
        title: str,
        description: Optional[str],
        priority: Priority,
        reporter_id: int,
        status: IssueStatus = IssueStatus.NEW,
    ) -> Issue:
        if not title or not reporter_id or not priority:
            raise ValueError("Title, priority and reporter ID are required")

        try:
            issue = self.repository.create(
                title, description, status, priority, reporter_id
            )
            return issue
        except IntegrityError:
            raise ValueError("Issue creation failed due to integrity constraint")
        except Exception as e:
            raise ValueError(f"Issue creation failed: {str(e)}")

    def get_issue_by_id(self, issue_id: int) -> Issue:
        issue = self.repository.find_by_id(issue_id)
        if not issue:
            raise ValueError(f"Issue with ID {issue_id} not found")
        return issue

    def get_all_issues(self) -> List[Issue]:
        return self.repository.get_all() or []

    def get_issues_by_reporter_id(self, reporter_id: int) -> List[Issue]:
        return self.repository.get_by_reporter_id(reporter_id) or []

    def get_issues_by_assignee_id(self, assignee_id: int) -> List[Issue]:
        return self.repository.get_by_assignee_id(assignee_id) or []

    def update_issue(
        self,
        issue_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[IssueStatus] = None,
        priority: Optional[Priority] = None,
        assignee_id: Optional[int] = None,
    ) -> Issue:
        try:
            updated_issue = self.repository.update(
                issue_id, title, description, status, priority, assignee_id
            )
            if not updated_issue:
                raise ValueError(f"Issue with ID {issue_id} not found")
            return updated_issue
        except IntegrityError:
            raise ValueError("Issue update failed due to integrity constraint")
        except Exception as e:
            raise ValueError(f"Issue update failed: {str(e)}")

    def delete_issue(self, issue_id: int) -> None:
        try:
            if not self.repository.delete(issue_id):
                raise ValueError(
                    f"Issue with ID {issue_id} not found or could not be deleted"
                )
        except Exception as e:
            raise ValueError(f"Issue deletion failed: {str(e)}")

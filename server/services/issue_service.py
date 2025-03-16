from exceptions import IssueServiceException
from repositories import IssueRepository
from typing import Optional
from models import Issue, IssueStatus, Priority
from sqlalchemy.exc import IntegrityError
from dto import Page


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
            raise IssueServiceException("Title, priority and reporter ID are required")

        try:
            issue = self.repository.create(
                title, description, status, priority, reporter_id
            )
            return issue
        except IntegrityError:
            raise ValueError("Issue creation failed due to integrity constraint")
        except Exception as e:
            raise IssueServiceException(f"Issue creation failed: {str(e)}")

    def get_issue_by_id(self, issue_id: int) -> Issue:
        issue = self.repository.find_by_id(issue_id)
        if not issue:
            raise ValueError(f"Issue with ID {issue_id} not found")
        return issue

    def get_all_issues(self) -> list[Issue]:
        return self.repository.get_all() or []

    def get_count_issues(self) -> int:
        return len(self.get_all_issues())

    def get_all_issues_paginated(
        self, page: int, elements_per_page: int
    ) -> Page[Issue]:
        issues = self.repository.get_all_paginated(page, elements_per_page) or []
        total_issues = self.get_count_issues()
        total_pages = (total_issues + elements_per_page - 1) // elements_per_page

        return Page(issues, total_issues, total_pages, page)

    def get_issues_by_reporter_id(
        self, reporter_id: int, page: int, elements_per_page: int
    ) -> Page[Issue]:
        issues = (
            self.repository.get_by_reporter_id(reporter_id, page, elements_per_page)
            or []
        )
        total_issues = self.get_count_issues()
        total_pages = (total_issues + elements_per_page - 1) // elements_per_page

        return Page(issues, total_issues, total_pages, page)

    def get_issues_by_assignee_id(
        self, assignee_id: int, page: int, elements_per_page: int
    ) -> Page[Issue]:
        issues = (
            self.repository.get_by_assignee_id(assignee_id, page, elements_per_page)
            or []
        )
        total_issues = self.get_count_issues()
        total_pages = (total_issues + elements_per_page - 1) // elements_per_page

        return Page(issues, total_issues, total_pages, page)

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
            raise IssueServiceException(f"Issue update failed: {str(e)}")

    def delete_issue(self, issue_id: int) -> None:
        try:
            if not self.repository.delete(issue_id):
                raise ValueError(
                    f"Issue with ID {issue_id} not found or could not be deleted"
                )
        except Exception as e:
            raise IssueServiceException(f"Issue deletion failed: {str(e)}")

    def assign_issue(self, issue_id: int, assignee_id: int) -> Issue:
        try:
            if not self.check_if_issue_exists_and_not_closed(issue_id):
                raise ValueError(f"Issue with ID {issue_id} not found")
            if self.check_if_issue_assigned(issue_id):
                raise IssueServiceException(
                    f"Issue with ID {issue_id} is already assigned"
                )
            in_progress_status = IssueStatus.IN_PROGRESS
            updated_issue = self.repository.assign_issue(
                issue_id, assignee_id, in_progress_status
            )
            if not updated_issue:
                raise ValueError(f"Issue with ID {issue_id} not found")
            return updated_issue
        except IntegrityError:
            raise ValueError("Issue assignment failed due to integrity constraint")
        except Exception as e:
            raise IssueServiceException(f"Issue assignment failed: {str(e)}")

    def check_if_issue_exists_and_not_closed(self, issue_id: int) -> bool:
        return self.repository.check_if_issue_exists_and_not_closed(issue_id)

    def check_if_user_is_assignee_or_reporter_of_issue(
        self, issue_id: int, user_id: int
    ) -> bool:
        return self.repository.check_if_user_is_assignee_or_reporter_of_issue(
            issue_id, user_id
        )

    def check_if_issue_assigned(self, issue_id: int) -> bool:
        return self.repository.check_if_issue_assigned(issue_id)

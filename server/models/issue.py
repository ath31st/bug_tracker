from models import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum
from datetime import datetime, timezone
from models.enums import IssueStatus, Priority


class Issue(db.Model):
    __tablename__ = "issues"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[IssueStatus] = mapped_column(
        Enum(IssueStatus), default=IssueStatus.NEW
    )
    priority: Mapped[Priority] = mapped_column(Enum(Priority), default=Priority.MEDIUM)
    reporter_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    assignee_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    reporter = relationship(
        "User", back_populates="created_issues", foreign_keys=[reporter_id]
    )
    assignee = relationship(
        "User", back_populates="assigned_issues", foreign_keys=[assignee_id]
    )
    comments = relationship("Comment", back_populates="issue", cascade="all, delete")

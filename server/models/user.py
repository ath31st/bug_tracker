from typing import List
from models import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    created_issues: Mapped[List["Issue"]] = relationship(
        "Issue", back_populates="reporter", foreign_keys="Issue.reporter_id"
    )
    assigned_issues: Mapped[List["Issue"]] = relationship(
        "Issue", back_populates="assignee", foreign_keys="Issue.assignee_id"
    )
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="author")

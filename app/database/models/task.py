from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import DateTime, Integer, Text, func, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base import Base
from app.enum.task import TaskStatus, TaskType


class Task(Base):
    """
    ORM class for Task
    """

    __tablename__ = "task"

    id: Mapped[str] = mapped_column("id", Text, primary_key=True, server_default=text("uuid_generate_v4()"))
    type: Mapped[TaskType] = mapped_column("type", Text, comment="Task type", index=True)
    result: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        "result", JSONB, comment="Result of the task execution", nullable=True
    )
    parameters: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        "parameters", JSONB, comment="Parameter of the task execution", nullable=True
    )
    error_message: Mapped[Optional[str]] = mapped_column("error_message", Text, comment="Error message of the task execution")
    error_code: Mapped[Optional[str]] = mapped_column("error_code", Integer, comment="Error Code of the task execution")
    status: Mapped[TaskStatus] = mapped_column(
        "status",
        Text,
        nullable=False,
        comment="The task status",
        server_default=text(f"'{TaskStatus.PENDING}'"),
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        "created_at",
        DateTime,
        comment="The time when the task was created",
        nullable=False,
        server_default=func.now(),
        index=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        "updated_at",
        DateTime,
        comment="The time when the task was updated",
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(
        "started_at", DateTime, comment="The time when the task was started", nullable=True
    )
    ended_at: Mapped[Optional[datetime]] = mapped_column(
        "ended_at", DateTime, comment="The time when the task was ended", nullable=True
    )

"""The schemas of task are defined in here."""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from app.enum.task import TaskStatus, TaskType


class BaseTask(BaseModel):
    """Task schema base for inherit and request body on POST API."""

    type: TaskType = Field(..., title="type", description="The type of task", example=TaskType.SLEEP)
    parameters: Dict[str, Any] = Field({}, title="parameters", description="The parameters of task", example={})


class Task(BaseTask):
    """Task schema for GET task API."""

    id: str = Field(
        ...,
        title="UUID of task",
        description="UUID of task",
        example="11111111-2222-4444-3333-555555555555",
    )
    result: Optional[Dict[str, Any]] = Field(
        None, title="result", description="The result of task", example={"summary": "something about meeting"}
    )
    error_code: Optional[str] = Field(None, title="error_message", description="The error_message of task", example=1)
    error_message: Optional[str] = Field(
        None, title="error_message", description="The error_message of task", example="The internal error."
    )
    status: TaskStatus = Field(..., title="status", description="The status of task", example=TaskStatus.PENDING)
    created_at: datetime = Field(
        ...,
        title="Task created_at",
        description="The UTC time when the task was initially created.<br>"
        "https://pydantic-docs.helpmanual.io/usage/types/#datetime-types",
        example="2020-06-09 10:25:47.116777",
    )
    updated_at: datetime = Field(
        ...,
        title="Task updated_at",
        description="The UTC time when the task was updated.<br>"
        "https://pydantic-docs.helpmanual.io/usage/types/#datetime-types",
        example="2020-06-09 10:25:47.116777",
    )
    started_at: Optional[datetime] = Field(
        None,
        title="Task started_at",
        description="The UTC time when the task was started.<br>"
        "https://pydantic-docs.helpmanual.io/usage/types/#datetime-types",
        example="2020-06-09 10:25:47.116777",
    )
    ended_at: Optional[datetime] = Field(
        None,
        title="Task ended_at",
        description="The UTC time when the task was ended.<br>"
        "https://pydantic-docs.helpmanual.io/usage/types/#datetime-types",
        example="2020-06-09 10:25:47.116777",
    )

    class Config:
        """Enable orm_mode."""

        orm_mode = True


class UpdateTask(BaseModel):
    """Update Task schema."""

    result: Optional[Dict[str, Any]] = Field(
        ..., title="result", description="The result of task", example={"summary": "something about meeting"}
    )
    error_message: Optional[str] = Field(
        ..., title="error_message", description="The error_message of task", example="internal error."
    )
    status: TaskStatus = Field(..., title="status", description="The status of task", example=TaskStatus.PENDING)
    started_at: Optional[datetime] = Field(
        ..., title="started_at", description="The started_at of task", example=datetime.now()
    )
    ended_at: Optional[datetime] = Field(..., title="ended_at", description="The ended_at of task", example=datetime.now())


class CreateTask(BaseTask):
    """Create Task schema."""

    pass

"""db operation for task"""

from datetime import datetime
from typing import Dict, List, Optional

from sqlalchemy import func, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.task import Task
from app.enum.task import TaskStatus, TaskType
from app.utils.db import as_order_by_expression
from app.utils.exceptions.db import EntryWithIDNotExist
from app.utils.logging.logger import get_logger

logger = get_logger()


async def create_task(
    db: AsyncSession,
    type: TaskType,
    status: TaskStatus = TaskStatus.PENDING,
    parameters: Optional[Dict[str, str]] = None,
    auto_commit: bool = True,
) -> Task:
    """
    Create a new Task
    """
    try:
        task = Task(
            type=type,
            status=status,
            parameters=parameters,
        )
        db.add(task)
        if auto_commit:
            await db.commit()
        await db.refresh(task)
        return task
    except Exception as e:
        if auto_commit:
            await db.rollback()
        logger.error(f"Failed to create task: {e}")
        raise e


async def list_tasks(
    db: AsyncSession,
    offset: int = 0,
    limit: int = 0,
    order_by: str = "created_at:desc",
    status_list: Optional[List[TaskStatus]] = None,
) -> List[Task]:
    """
    Get tasks by conditions
    """
    query = select(Task)
    if status_list is not None:
        query = query.where(Task.status.in_(status_list))
    if offset:
        query = query.offset(offset)
    if limit:
        query = query.limit(limit)
    for expression in as_order_by_expression(Task, order_by):
        query = query.order_by(expression)

    result = await db.execute(query)
    return list(result.scalars().all())


async def count_tasks(
    db: AsyncSession,
    status_list: Optional[List[TaskStatus]] = None,
) -> int:
    """
    Get tasks by conditions
    """
    query = select(func.count()).select_from(Task)
    if status_list is not None:
        query = query.where(Task.status.in_(status_list))
    result = await db.execute(query)
    return result.scalars().one()


async def update_task(
    db: AsyncSession,
    task_id: str,
    result: Optional[Dict[str, str]] = None,
    status: Optional[TaskStatus] = None,
    error_message: Optional[str] = None,
    started_at: Optional[datetime] = None,
    ended_at: Optional[datetime] = None,
    auto_commit: bool = True,
) -> Task:
    """
    Update the task by id
    """
    data = {}
    if result:
        data["result"] = result
    if status:
        data["status"] = status
    if error_message:
        data["error_message"] = error_message
    if started_at:
        data["started_at"] = started_at
    if ended_at:
        data["ended_at"] = ended_at

    query = update(Task).values(**data).where(Task.id == task_id).returning(Task)
    try:
        task = (await db.execute(query)).scalars().one()
        if auto_commit:
            await db.commit()
        return task
    except NoResultFound:
        if auto_commit:
            await db.rollback()
        raise EntryWithIDNotExist(entry_name=Task.__tablename__, id=task_id)

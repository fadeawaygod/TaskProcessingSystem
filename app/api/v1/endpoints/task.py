"""
Definition of the task endpoints for the service.
"""

from typing import Union

import redis
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schema.generic import ListResponse
from app.api.v1.schema.task import CreateTask, Task
from app.database.crud import task as crud_task
from app.database.models.task import Task as TaskModel
from app.middleware.depends import get_db_session, get_redis_session
from app.utils.logging.logger import get_logger
from app.utils.task.task import create_and_publish_task

logger = get_logger()
router: APIRouter = APIRouter()


@router.post(
    "",
    description="Create a task.",
    response_model=Task,
)
async def post_task(
    request_body: CreateTask,
    db: AsyncSession = Depends(get_db_session),
    redis: Union[redis.Redis, redis.RedisCluster] = Depends(get_redis_session),
) -> Task:

    task = await create_and_publish_task(
        db=db,
        redis=redis,
        type=request_body.type,
        parameters=request_body.parameters,
    )
    return task


@router.get(
    "",
    response_model=ListResponse[Task],
    description="List all tasks",
)
async def get_tasks(
    offset: int = Query(
        0,
        description="Optional, determine the number of rows need be skipped",
        example=0,
    ),
    limit: int = Query(
        0,
        description="Optional, determine the number of returned rows after skipped offset, if it is 0, return all items",
        example=0,
    ),
    order_by: str = Query(
        "created_at:desc",
        description="Optional, order items by asc or desc with comma-separated list of : pairs, default is created_at:desc.",
        example="created_at:desc",
    ),
    db: AsyncSession = Depends(get_db_session),
) -> ListResponse[Task]:
    """
    List tasks by filter
    """
    tasks = await crud_task.list_tasks(
        db,
        offset=offset,
        limit=limit,
        order_by=order_by,
    )
    tasks_total = await crud_task.count_tasks(
        db=db,
    )
    return ListResponse(data=tasks, total=tasks_total)
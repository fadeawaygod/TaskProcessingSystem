import json
from typing import Dict, Optional, Union

import redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.crud import task as crud_task
from app.database.models.task import Task
from app.enum.task import TaskStatus, TaskType
from app.utils.logging.logger import get_logger

logger = get_logger()

TASK_QUEUE_NAME = "Task_processing_system:task_queue"


async def create_and_publish_task(
    db: AsyncSession,
    redis: Union[redis.Redis, redis.RedisCluster],
    type: TaskType,
    parameters: Optional[Dict[str, str]] = None,
) -> Task:
    """
    Create a new task and submit it to the executor.

    Args:
        db: The sqlalchemy AsyncSession.
        type: The type of task to create.
        parameters: Optional parameters to pass to the task.
    Returns:
        The newly created and submitted task.
    """
    task = await crud_task.create_task(db=db, type=type, status=TaskStatus.PENDING, parameters=parameters)
    await publish_task_to_queue(redis=redis, queue_name=TASK_QUEUE_NAME, task_id=task.id)
    return task


async def publish_task_to_queue(
    redis: Union[redis.Redis, redis.RedisCluster],
    queue_name: str,
    task_id: str,
):
    message = {"task_id": task_id}
    try:
        await redis.xadd(queue_name, fields=message)  # type: ignore
        logger.info(f"Message value {message} published to queue({queue_name})")
    except Exception as e:
        logger.error(f"Failed to publish message value {message} to queue({queue_name}), error:{e}.")
        raise e

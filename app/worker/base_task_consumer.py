import asyncio
import time
import uuid
from typing import Dict, List, Optional, Union

import redis.asyncio as async_redis
from redis import ResponseError

from app.database.crud import task as crud_task
from app.database.models.task import Task
from app.enum.task import TaskStatus, TaskType
from app.middleware.depends import get_db_session_context_manager
from app.utils.logging.logger import get_logger
from app.utils.time import get_utc_now_without_timezone
from app.worker.task_handler.base_handler import BaseHandler

DEFAULT_READ_MESSAGE_COUNT = 1
CLAIM_RETRY_INTERVAL = 1
XGROUPCREATE_SPECIAL_ID = "$"
XREADGROUP_SPECIAL_ID = ">"
XREADGROUP_BLOCK_MS = 3 * 1000
XREADGROUP_DEFAULT_COUNT = 1
XPENDING_START = "-"
XPENDING_END = "+"
XPENDING_DEFAULT_COUNT = 1
MIN_IDLE_TIME_MS = 10 * 1000
MESSAGE_LIMIT_LENGTH = 1024

logger = get_logger()


class BaseTaskConsumer:
    """The abstract Base Task Consumer class. Used to consume task messages from the event bus system."""

    def __init__(
        self,
        redis_connection: Union[async_redis.Redis, async_redis.RedisCluster],
        task_handlers: Dict[TaskType, BaseHandler],
        queue_name: str,
        consumer_group_name: str = "default_group",
        max_retry_count: int = 3,
    ):

        self._redis_connection = redis_connection
        self._task_handlers = task_handlers
        self._stream_name = queue_name
        self._consumer_group_name = consumer_group_name
        self._consumer_name = f"{consumer_group_name}_{uuid.uuid4()}"
        self._task = None
        self._max_retry_count = max_retry_count

    async def run(self):
        """Continuously runs the EventBusConsumer to handle pending and new messages."""
        await self._create_consumer_group_if_not_exists()
        retried_count = 0
        while True:
            messages = []
            try:
                messages = await self._auto_claim_messages(count=DEFAULT_READ_MESSAGE_COUNT)
                retried_count = 0
                if not messages:
                    messages = await self._get_new_messages(count=DEFAULT_READ_MESSAGE_COUNT)
            except KeyboardInterrupt:
                logger.info(f"KeyboardInterrupt, stop the consumer group({self._consumer_group_name})")
                break
            except Exception as e:
                logger.error(f"TaskConsumer: Failed to retrieve message, error: {e}")
                if retried_count >= self._max_retry_count:
                    logger.error(
                        f"TaskConsumer: Failed to retrieve message after {retried_count} retries, stop the consumer group({self._consumer_group_name})"
                    )
                    break
                await asyncio.sleep(2**retried_count - 1)
                retried_count += 1
                continue

            for message in messages:
                await self._process_message(message=message)

    async def _create_consumer_group_if_not_exists(self):
        groups = []
        try:
            groups = await self._redis_connection.xinfo_groups(self._stream_name)
        except ResponseError as e:
            if str(e) == "no such key":
                groups = []
            else:
                raise e

        group = next((group for group in groups if group["name"] == self._consumer_group_name), None)
        if not group:
            logger.info(f"Create a new group({self._consumer_group_name}) in stream({self._stream_name})")
            await self._redis_connection.xgroup_create(
                name=self._stream_name,
                groupname=self._consumer_group_name,
                id=XGROUPCREATE_SPECIAL_ID,
                mkstream=True,
            )

        return self

    async def _auto_claim_messages(
        self, count: Optional[int] = XPENDING_DEFAULT_COUNT, min_idle_time: int = MIN_IDLE_TIME_MS
    ) -> List[dict]:
        _, claimed_messages, _ = await self._redis_connection.xautoclaim(
            name=self._stream_name,
            groupname=self._consumer_group_name,
            consumername=self._consumer_name,
            min_idle_time=min_idle_time,
            count=count,
        )
        return claimed_messages

    async def _get_new_messages(
        self, block_time: Optional[int] = XREADGROUP_BLOCK_MS, count: Optional[int] = XREADGROUP_DEFAULT_COUNT
    ) -> List[dict]:
        new_messages = await self._redis_connection.xreadgroup(
            groupname=self._consumer_group_name,
            consumername=self._consumer_name,
            streams={self._stream_name: XREADGROUP_SPECIAL_ID},
            count=count,
            block=block_time,
        )
        results = []
        for queue_messages in new_messages:
            _, messages, *_ = queue_messages
            results.extend(messages)

        return results

    async def _ack_message(self, message_id: str):
        try:
            await self._redis_connection.xack(self._stream_name, self._consumer_group_name, message_id)
            logger.info(f"Acknowledged message({message_id}).")
        except Exception as e:
            logger.error(f"Failed to acknowledge message({message_id}), error:{e}")

    async def _on_start(self, task: Task):
        logger.info(f"Task id: {task.id} started.")
        async with get_db_session_context_manager() as db:
            await crud_task.update_task(
                db=db,
                task_id=task.id,
                status=TaskStatus.PROCESSING,
                started_at=get_utc_now_without_timezone(),
            )

    async def _on_finish(self, task: Task):
        logger.info(f"Task id: {task.id} finished.")
        async with get_db_session_context_manager() as db:
            await crud_task.update_task(
                db=db,
                task_id=task.id,
                status=TaskStatus.COMPLETED,
                ended_at=get_utc_now_without_timezone(),
            )

    async def _on_error(self, task: Task, error: Exception):
        logger.warning(f"Task id: {task.id} raised an error: {error.__class__.__name__} {error}.")
        async with get_db_session_context_manager() as db:
            await crud_task.update_task(
                db=db,
                task_id=task.id,
                status=TaskStatus.FAILED,
                ended_at=get_utc_now_without_timezone(),
                error_message=str(error),
                error_code=getattr(error, "code", 1),
            )

    async def _process_message(
        self,
        message: dict,
    ):
        try:
            message_id, task_payload = message
            async with get_db_session_context_manager() as db:
                self._task = await crud_task.get_task(db=db, id=task_payload["task_id"])
            if self._task.status == TaskStatus.PENDING:
                try:
                    handler = self._task_handlers.get(self._task.type)
                    if not handler:
                        logger.error(f"TaskConsumer: Failed to get handler for task type: {self._task.type}")
                        raise Exception(f"TaskConsumer: Failed to get handler for task type: {self._task.type}")
                    await self._on_start(self._task)
                    start_time = time.time()
                    await handler.handle(self._task)
                    logger.info(
                        f"TaskConsumer: Task id: {self._task.id} finished, time elapsed: " f"{time.time() - start_time }s"
                    )
                    await self._on_finish(self._task)
                except Exception as e:
                    await self._on_error(self._task, e)
            else:
                logger.warning(f"The task: {self._task.id} is in {self._task.status}, skip it")
            await self._ack_message(message_id)
        except Exception as e:
            logger.error(f"TaskConsumer: Failed to process message: {message}, error:{e}")

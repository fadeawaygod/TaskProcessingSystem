import asyncio

from app.const.task import TASK_QUEUE_NAME
from app.core.config import settings
from app.enum.task import TaskType
from app.utils.logging.logger import get_logger
from app.utils.redis import setup_redis_connection
from app.worker.base_task_consumer import BaseTaskConsumer
from app.worker.task_handler.sleep_handler import SleepHandler

logger = get_logger()


async def async_main():
    logger.info("Start API Server worker")
    task_consumer = BaseTaskConsumer(
        redis_connection=setup_redis_connection(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            is_cluster=settings.IS_REDIS_CLUSTER,
        ),
        queue_name=TASK_QUEUE_NAME,
        task_handlers={
            TaskType.SLEEP: SleepHandler(),  # type: ignore
        },
    )
    await task_consumer.run()


if __name__ == "__main__":
    asyncio.run(async_main())

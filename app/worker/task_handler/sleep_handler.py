import asyncio

from app.database.models.task import Task as TaskModel
from app.utils.logging.logger import get_logger
from app.worker.task_handler.base_handler import BaseHandler

logger = get_logger()


class SleepHandler(BaseHandler):

    async def handle(self, task: TaskModel):
        await asyncio.sleep(3)  # mock heavy operation

from app.database.models.task import Task as TaskModel


class BaseHandler:
    """Base worker class for running tasks."""

    async def handle(self, task: TaskModel):
        """Handle the task, all handlers should implement this."""
        raise NotImplementedError()

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from redis.exceptions import ConnectionError
from sqlalchemy.exc import SQLAlchemyError

from app.database.models.task import Task
from app.enum.task import TaskStatus, TaskType
from app.worker.base_task_consumer import BaseTaskConsumer
from tests.unit_test.utils import _make_fake_redis_connection, make_fake_db_async_context_manager


@pytest.mark.asyncio
async def test_run_normally():
    def get_execute_side_effect():
        mock_result_1 = MagicMock()
        mock_scalars_1 = MagicMock()
        mock_scalars_1.all.return_value = [
            Task(
                id="test",
                status=TaskStatus.PENDING,
                type=TaskType.SLEEP,
                parameters={},
                result={},
                created_at="2022-01-01 00:00:00",
                updated_at="2022-01-01 00:00:00",
                started_at="2022-01-01 00:00:00",
                ended_at="2022-01-01 00:00:00",
            )
        ]
        mock_result_1.scalars.return_value = mock_scalars_1

        mock_result_2 = MagicMock()
        mock_scalars_2 = MagicMock()
        mock_scalars_2.one.return_value = 1
        mock_result_2.scalars.return_value = mock_scalars_2

        mock_execute_side_effect = [mock_result_1]
        return mock_execute_side_effect

    db_execute_side_effect = get_execute_side_effect()
    with patch(
        "app.worker.base_task_consumer.get_db_session_context_manager",
        return_value=make_fake_db_async_context_manager(execute_side_effect=db_execute_side_effect),
    ):
        fake_redis_connection = _make_fake_redis_connection()
        await BaseTaskConsumer(
            redis_connection=fake_redis_connection,  # type: ignore
            task_handlers={TaskType.SLEEP: AsyncMock()},
            queue_name="test",
        ).run()
    fake_redis_connection.xautoclaim.assert_called()
    fake_redis_connection.xgroup_create.assert_called_once()
    fake_redis_connection.xinfo_groups.assert_called_once()


@pytest.mark.asyncio
async def test_run_redis_connection_error_should_retry():
    def get_execute_side_effect():
        mock_result_1 = MagicMock()
        mock_scalars_1 = MagicMock()
        mock_scalars_1.all.return_value = [
            Task(
                id="test",
                status=TaskStatus.PENDING,
                type=TaskType.SLEEP,
                parameters={},
                result={},
                created_at="2022-01-01 00:00:00",
                updated_at="2022-01-01 00:00:00",
                started_at="2022-01-01 00:00:00",
                ended_at="2022-01-01 00:00:00",
            )
        ]
        mock_result_1.scalars.return_value = mock_scalars_1

        mock_result_2 = MagicMock()
        mock_scalars_2 = MagicMock()
        mock_scalars_2.one.return_value = 1
        mock_result_2.scalars.return_value = mock_scalars_2

        mock_execute_side_effect = [mock_result_1]
        return mock_execute_side_effect

    db_execute_side_effect = get_execute_side_effect()
    with patch(
        "app.worker.base_task_consumer.get_db_session_context_manager",
        return_value=make_fake_db_async_context_manager(execute_side_effect=db_execute_side_effect),
    ):
        fake_redis_connection = _make_fake_redis_connection(xautoclaim_side_effect=[ConnectionError()])
        await BaseTaskConsumer(
            redis_connection=fake_redis_connection,  # type: ignore
            task_handlers={TaskType.SLEEP: AsyncMock()},
            queue_name="test",
            max_retry_count=1,
        ).run()
    assert fake_redis_connection.xautoclaim.call_count == 2


@pytest.mark.asyncio
async def test_run_db_connection_error_should_not_ack():
    db_execute_side_effect = [SQLAlchemyError()]
    with patch(
        "app.worker.base_task_consumer.get_db_session_context_manager",
        return_value=make_fake_db_async_context_manager(execute_side_effect=db_execute_side_effect),
    ):
        fake_redis_connection = _make_fake_redis_connection()
        await BaseTaskConsumer(
            redis_connection=fake_redis_connection,  # type: ignore
            task_handlers={TaskType.SLEEP: AsyncMock()},
            queue_name="test",
            max_retry_count=1,
        ).run()
    fake_redis_connection.xack.assert_not_called()


@pytest.mark.asyncio
async def test_run_cancelled_should_not_run_but_ack():
    def get_execute_side_effect():
        mock_result_1 = MagicMock()
        mock_scalars_1 = MagicMock()
        mock_scalars_1.all.return_value = [
            Task(
                id="test",
                status=TaskStatus.CANCELED,
                type=TaskType.SLEEP,
                parameters={},
                result={},
                created_at="2022-01-01 00:00:00",
                updated_at="2022-01-01 00:00:00",
                started_at="2022-01-01 00:00:00",
                ended_at="2022-01-01 00:00:00",
            )
        ]
        mock_result_1.scalars.return_value = mock_scalars_1

        mock_result_2 = MagicMock()
        mock_scalars_2 = MagicMock()
        mock_scalars_2.one.return_value = 1
        mock_result_2.scalars.return_value = mock_scalars_2

        mock_execute_side_effect = [mock_result_1]
        return mock_execute_side_effect

    fake_db_async_context_manager = make_fake_db_async_context_manager(execute_side_effect=get_execute_side_effect())
    with patch(
        "app.worker.base_task_consumer.get_db_session_context_manager",
        return_value=fake_db_async_context_manager,
    ):
        fake_redis_connection = _make_fake_redis_connection()
        await BaseTaskConsumer(
            redis_connection=fake_redis_connection,  # type: ignore
            task_handlers={TaskType.SLEEP: AsyncMock()},
            queue_name="test",
        ).run()
    fake_redis_connection.xautoclaim.assert_called()
    fake_redis_connection.xgroup_create.assert_called_once()
    fake_redis_connection.xinfo_groups.assert_called_once()
    fake_redis_connection.xack.assert_called_once()

    fake_db_session = fake_db_async_context_manager.__aenter__.return_value
    fake_db_session.commit.assert_not_called()

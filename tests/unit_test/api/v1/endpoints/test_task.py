from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient
from redis.exceptions import ConnectionError
from sqlalchemy.exc import SQLAlchemyError

from app.database.models.task import Task
from app.enum.task import TaskStatus, TaskType
from app.main import app
from app.utils.exceptions.task import JobCannotBeCancelled
from tests.unit_test.utils import override_get_db, override_get_redis

client = TestClient(app)  # type: ignore


@pytest.mark.asyncio
async def test_get_tasks_normal_return():
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

        mock_execute_side_effect = [mock_result_1, mock_result_2]
        return mock_execute_side_effect

    with override_get_db(
        app=app,
        execute_side_effect=get_execute_side_effect(),
    ):
        response = client.get("/api/v1/tasks")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json == {
        "total": 1,
        "data": [
            {
                "type": "SLEEP",
                "parameters": {},
                "id": "test",
                "result": {},
                "error_code": None,
                "error_message": None,
                "status": "PENDING",
                "created_at": "2022-01-01T00:00:00",
                "updated_at": "2022-01-01T00:00:00",
                "started_at": "2022-01-01T00:00:00",
                "ended_at": "2022-01-01T00:00:00",
            }
        ],
    }


@pytest.mark.asyncio
async def test_get_tasks_db_connection_failed():
    with override_get_db(
        app=app,
        execute_side_effect=[SQLAlchemyError("Connection failed")],
    ):
        with pytest.raises(SQLAlchemyError):
            client.get("/api/v1/tasks")


@pytest.mark.asyncio
async def test_post_tasks_normal_result():
    with override_get_db(
        app=app,
        commit_side_effect=[AsyncMock()],
        fake_refresh=_fake_refresh_for_create_task,  # type: ignore
    ):
        with override_get_redis(app=app):
            response = client.post(
                "/api/v1/tasks",
                json={
                    "type": "SLEEP",
                },
            )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_post_tasks_db_connection_failed():
    with override_get_db(
        app=app,
        commit_side_effect=[SQLAlchemyError("Connection failed")],
    ):
        with override_get_redis(app=app):
            with pytest.raises(SQLAlchemyError):
                client.post(
                    "/api/v1/tasks",
                    json={
                        "type": "SLEEP",
                    },
                )


@pytest.mark.asyncio
async def test_post_tasks_redis_connection_failed():
    with override_get_db(
        app=app,
        commit_side_effect=[AsyncMock()],
        fake_refresh=_fake_refresh_for_create_task,  # type: ignore
    ):
        with override_get_redis(app=app, xadd_side_effect=[ConnectionError("Error 111 connecting to 127.0.0.1:6379. 111.")]):
            with pytest.raises(ConnectionError):
                client.post(
                    "/api/v1/tasks",
                    json={
                        "type": "SLEEP",
                    },
                )


@pytest.mark.asyncio
async def test_post_tasks_no_type_in_request():
    with override_get_db(app=app):
        with override_get_redis(app=app):
            response = client.post(
                "/api/v1/tasks",
                data={
                    "parameters": {},
                },
            )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_post_cancel_task_normal():
    with override_get_db(
        app=app,
        execute_side_effect=_get_execute_side_effect_for_post_cancel(),
        commit_side_effect=[AsyncMock()],
    ):
        with override_get_redis(app=app):
            response = client.post(
                "/api/v1/tasks/test-id/cancel",
            )
    assert response.status_code == 200
    assert response.json()["status"] == TaskStatus.CANCELED


@pytest.mark.asyncio
async def test_post_cancel_task_status_completed_should_fail():
    def get_execute_side_effect():
        mock_result_1 = MagicMock()
        mock_scalars_1 = MagicMock()
        mock_scalars_1.one.return_value = Task(
            id="test",
            status=TaskStatus.COMPLETED,
            type=TaskType.SLEEP,
            parameters={},
            result={},
            created_at="2022-01-01 00:00:00",
            updated_at="2022-01-01 00:00:00",
            started_at="2022-01-01 00:00:00",
            ended_at="2022-01-01 00:00:00",
        )
        mock_result_1.scalars.return_value = mock_scalars_1

        mock_execute_side_effect = [mock_result_1]

        return mock_execute_side_effect

    with override_get_db(
        app=app,
        execute_side_effect=get_execute_side_effect(),
        commit_side_effect=[AsyncMock()],
    ):
        with override_get_redis(app=app):
            with pytest.raises(JobCannotBeCancelled):
                client.post(
                    "/api/v1/tasks/test-id/cancel",
                )


@pytest.mark.asyncio
async def test_post_cancel_tasks_db_connection_failed():
    with override_get_db(
        app=app,
        execute_side_effect=[SQLAlchemyError("Connection failed")],
    ):
        with override_get_redis(app=app):
            with pytest.raises(SQLAlchemyError):
                client.post(
                    "/api/v1/tasks/test-id/cancel",
                )


async def _fake_refresh_for_create_task(task: Task):
    task.id = "test"
    task.created_at = "2022-01-01 00:00:00"  # type: ignore
    task.updated_at = "2022-01-01 00:00:00"  # type: ignore


def _get_execute_side_effect_for_post_cancel():
    mock_result_1 = MagicMock()
    mock_scalars_1 = MagicMock()
    mock_scalars_1.one.return_value = Task(
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

    mock_result_1.scalars.return_value = mock_scalars_1

    mock_result_for_update_task = MagicMock()
    mock_scalars_2 = MagicMock()
    mock_scalars_2.one.return_value = Task(
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

    mock_result_for_update_task.scalars.return_value = mock_scalars_2
    mock_execute_side_effect = [mock_result_1, mock_result_for_update_task]

    return mock_execute_side_effect

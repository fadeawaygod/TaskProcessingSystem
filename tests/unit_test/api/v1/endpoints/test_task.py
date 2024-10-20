from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

from app.database.models.task import Task
from app.enum.task import TaskStatus, TaskType
from app.main import app
from tests.unit_test.utils import override_get_db

client = TestClient(app)  # type: ignore


@pytest.mark.asyncio
async def test_get_tasks_normal_return():
    def get_execute_side_effect():
        mock_session = AsyncMock()

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

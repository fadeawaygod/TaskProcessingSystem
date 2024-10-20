from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from app.database.models.task import Task
from app.enum.task import TaskStatus, TaskType
from app.main import app
from app.middleware.depends import get_db_session

client = TestClient(app)  # type: ignore


@pytest.fixture
def mock_db_session():
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
        )
    ]
    mock_result_1.scalars.return_value = mock_scalars_1
    mock_session.execute.return_value = mock_result_1

    mock_result_2 = MagicMock()
    mock_scalars_2 = MagicMock()
    mock_scalars_2.one.return_value = 1
    mock_result_2.scalars.return_value = mock_scalars_2
    mock_session.execute.return_value = mock_result_2

    mock_execute_side_effect = [mock_result_1, mock_result_2]
    mock_session.execute.side_effect = mock_execute_side_effect
    return mock_session


@pytest.fixture
def override_get_db(mock_db_session):
    app.dependency_overrides[get_db_session] = lambda: mock_db_session
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_tasks(override_get_db):
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

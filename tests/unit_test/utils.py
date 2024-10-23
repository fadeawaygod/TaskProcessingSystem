from contextlib import contextmanager
from typing import Any, Awaitable, Coroutine, List
from unittest.mock import AsyncMock, MagicMock

from fastapi import FastAPI

from app.middleware.depends import get_db_session, get_redis_session


@contextmanager
def override_get_db(
    app: FastAPI,
    execute_side_effect: List[Any] = [AsyncMock()],
    commit_side_effect: List[Any] = [AsyncMock()],
    fake_refresh: Coroutine = AsyncMock(),
):
    mock_session = AsyncMock()
    mock_session.execute.side_effect = execute_side_effect
    mock_session.commit.side_effect = commit_side_effect
    # add this line to prevent warning
    mock_session.add = MagicMock()
    mock_session.refresh = fake_refresh
    app.dependency_overrides[get_db_session] = lambda: mock_session
    yield
    app.dependency_overrides.clear()


@contextmanager
def override_get_redis(app: FastAPI, xadd_side_effect: List[Any] = [AsyncMock()]):
    mock_session = AsyncMock()
    mock_session.xadd.side_effect = xadd_side_effect
    app.dependency_overrides[get_redis_session] = lambda: mock_session
    yield
    app.dependency_overrides.clear()

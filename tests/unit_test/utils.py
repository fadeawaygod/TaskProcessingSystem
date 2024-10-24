from contextlib import contextmanager
from typing import Any, Coroutine, List
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


def make_fake_db_async_context_manager(
    execute_side_effect: List[Any] = [AsyncMock()],
    commit_side_effect: List[Any] = [AsyncMock()],
    fake_refresh: Coroutine = AsyncMock(),
):
    mock_session = AsyncMock()
    mock_session.execute.side_effect = execute_side_effect
    mock_session.commit.side_effect = commit_side_effect
    mock_session.add = MagicMock()
    mock_session.refresh = fake_refresh

    mock_async_context_manager = AsyncMock()
    mock_async_context_manager.__aenter__.return_value = mock_session
    return mock_async_context_manager


@contextmanager
def override_get_redis(app: FastAPI, xadd_side_effect: List[Any] = [AsyncMock()]):
    app.dependency_overrides[get_redis_session] = lambda: _make_fake_redis_connection(xadd_side_effect)
    yield
    app.dependency_overrides.clear()


def _make_fake_redis_connection(
    xadd_side_effect: List[Any] = [AsyncMock()],
    xautoclaim_side_effect: List[Any] = [
        (
            None,
            [("message_id", {"task_id": "test_task_id"})],
            None,
        ),
        KeyboardInterrupt(),
    ],
    xreadgroup_side_effect: List[Any] = [{}],
    xgroup_create_side_effect: List[Any] = [[]],
    xinfo_groups_side_effect: List[Any] = [AsyncMock()],
    xack_side_effect: List[Any] = [],
):
    mock_session = AsyncMock()
    mock_session.xadd.side_effect = xadd_side_effect
    mock_session.xautoclaim.side_effect = xautoclaim_side_effect
    mock_session.xreadgroup.side_effect = xreadgroup_side_effect
    mock_session.xgroup_create.side_effect = xgroup_create_side_effect
    mock_session.xinfo_groups.side_effect = xinfo_groups_side_effect
    mock_session.xack.side_effect = xack_side_effect
    return mock_session

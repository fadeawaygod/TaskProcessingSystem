from contextlib import contextmanager
from typing import Any, List
from unittest.mock import AsyncMock, MagicMock

from fastapi import FastAPI

from app.middleware.depends import get_db_session


@contextmanager
def override_get_db(app: FastAPI, execute_side_effect: List[Any] = []):
    mock_session = AsyncMock()
    mock_session.execute.side_effect = execute_side_effect
    app.dependency_overrides[get_db_session] = lambda: mock_session
    yield
    app.dependency_overrides.clear()

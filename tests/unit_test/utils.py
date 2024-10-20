from contextlib import contextmanager
from typing import List
from unittest.mock import MagicMock

from fastapi import FastAPI

from app.middleware.depends import get_db_session


@contextmanager
def override_get_db(app: FastAPI, execute_side_effect: List[MagicMock] = []):
    app.dependency_overrides[get_db_session] = lambda: execute_side_effect
    yield
    app.dependency_overrides.clear()

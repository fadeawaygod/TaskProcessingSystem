import time
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Union

import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.database.db import session_factory
from app.utils.logging.logger import get_logger
from app.utils.redis import setup_redis_connection

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 6379
DEFAULT_SOCKET_TIMEOUT = 5
DEFAULT_SOCKET_CONNECT_TIMEOUT = 3
DEFAULT_HEALTH_CHECK_INTERVAL = 10

logger = get_logger()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Return a async database session."""
    start_time = time.time()
    async with session_factory() as session:
        got_db_time = time.time()
        logger.debug((f"opened a db session: {id(session)}, time elapsed: {got_db_time-start_time:.3f}s"))
        try:
            yield session
        finally:
            await session_factory.remove()
            logger.debug(f"closed the db session: {id(session)} " f"time elapsed: {time.time() - got_db_time:.3f}s")


get_db_session_context_manager = asynccontextmanager(get_db_session)


def get_redis_session() -> Union[redis.Redis, redis.RedisCluster]:
    """Get a redis session.
    Returns:
        Union[redis.Redis, redis.RedisCluster]: [description]
    """  # noqa
    return global_redis_session


global_redis_session = setup_redis_connection(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    is_cluster=settings.IS_REDIS_CLUSTER,
    retry_on_error=[ConnectionError, TimeoutError],
)

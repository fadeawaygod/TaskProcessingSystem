"""
Utils about accessing Redis asyncronously.
"""

from typing import List, Optional, Type, Union

import redis.asyncio as redis
from redis.asyncio.cluster import ClusterNode

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 6379
DEFAULT_SOCKET_TIMEOUT = 5
DEFAULT_SOCKET_CONNECT_TIMEOUT = 3
DEFAULT_HEALTH_CHECK_INTERVAL = 10


def setup_redis_connection(
    host: Optional[str] = None,
    port: Optional[int] = None,
    is_cluster: bool = True,
    socket_timeout: Optional[float] = DEFAULT_SOCKET_TIMEOUT,
    socket_connect_timeout: Optional[float] = DEFAULT_SOCKET_CONNECT_TIMEOUT,
    retry_on_error: Optional[List[Type[Exception]]] = None,
) -> Union[redis.Redis, redis.RedisCluster]:
    """Get redis connection.

    Args:
        host (str): Server hostname. (default: `None`)
        port (int): Server port. (default: `None`)
        is_cluster (bool): Has true to enable cluster mode. (default: `True`)
        socket_timeout (float): Redis socket timeout (default: `DEFAULT_SOCKET_TIMEOUT`)
        socket_connect_timeout (float): Redis socket connect timeout. (default: `DEFAULT_SOCKET_CONNECT_TIMEOUT`)
        retry_on_error (List[Type[Exception]]): Specify errors for retrying. Redis client has default errors(ConnectionError and TimeoutError) for retrying. (default: `None`)

    Returns:
        Union[redis.Redis, redis.RedisCluster]: [description]
    """  # noqa
    host = host or DEFAULT_HOST
    port = port or DEFAULT_PORT
    if is_cluster:
        redis_connection = redis.RedisCluster(
            startup_nodes=[ClusterNode(host=host, port=port)],
            decode_responses=True,
            socket_timeout=socket_timeout,
            socket_connect_timeout=socket_connect_timeout,
            health_check_interval=DEFAULT_HEALTH_CHECK_INTERVAL,
            retry_on_error=retry_on_error,
        )  # type: ignore
    else:
        redis_connection = redis.Redis(
            host=host,
            port=port,
            decode_responses=True,
            socket_timeout=socket_timeout,
            socket_connect_timeout=socket_connect_timeout,
            health_check_interval=DEFAULT_HEALTH_CHECK_INTERVAL,
            retry_on_error=retry_on_error,
        )

    return redis_connection

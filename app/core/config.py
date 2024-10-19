from typing import Any, Dict, List, Optional, Union

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    """Extract env variables to app settings."""

    BACKEND_CORS_ORIGINS: Union[List[str], str] = []
    API_ROOT_PATH: str = ""
    APP_VERSION: str = "0.0.1"

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # K8s configuration
    NAMESPACE: Optional[str] = None

    # database
    # enable this if you want to build a new db in your local
    DO_INIT_DB: bool = False
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URI: Optional[PostgresDsn] = None
    DB_POOL_SIZE: int = 40
    DB_MAX_OVERFLOW: int = 10

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        """Assemble db connection uri if no DATABASE_URI env variables."""
        if v:
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST", ""),
            port=values.get("POSTGRES_PORT", ""),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # redis
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    IS_REDIS_CLUSTER: bool = False

    class Config:  # type: ignore
        case_sensitive = True
        env_file = ".env"


settings = Settings()

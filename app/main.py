from contextlib import asynccontextmanager
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.api import health
from app.api.v1.api import api_router
from app.core.config import settings
from app.database.init_db import init_db
from app.utils.logging.logger import get_logger
from app.utils.middleware.app_version import AppVersionMiddleware

DEFAULT_ERROR_CODE = 1
DEFAULT_RESPONSE_HEADER = {"Access-Control-Allow-Origin": "*"}
API_V1_STR: str = "/api/v1"


def get_application() -> FastAPI:
    """Get the FAST API application."""
    _app = FastAPI(
        title="Task Processing System",
        root_path=settings.API_ROOT_PATH,
        lifespan=lifespan,
    )
    _app.include_router(health.router, prefix="/health")
    _app.include_router(
        api_router,
        prefix=API_V1_STR,
    )
    # Middlewares
    _app.add_middleware(AppVersionMiddleware, app_version=settings.APP_VERSION)
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return _app


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.DO_INIT_DB:
        await init_db(app)
    logger.info("local swagger url: http://0.0.0.0:8000/docs")
    yield


logger = get_logger()
app = get_application()


@app.exception_handler(Exception)
async def exception_handler(request: Request, exception: Exception) -> JSONResponse:
    """Handle other exceptions."""
    logger.warning(
        f"The request {request.method + ' ' + str(request.url) if request else ''} raised an exception: "
        f"{exception.__class__.__name__}, {exception}"
    )
    response = {
        "detail": exception.message if hasattr(exception, "message") else str(exception),  # type: ignore
        "code": exception.code if hasattr(exception, "code") else DEFAULT_ERROR_CODE,  # type: ignore
        "parameters": exception.parameters if hasattr(exception, "parameters") else {},  # type: ignore
    }
    status_code = exception.status_code if hasattr(exception, "status_code") else HTTPStatus.INTERNAL_SERVER_ERROR  # type: ignore
    return JSONResponse(content=response, status_code=status_code, headers=DEFAULT_RESPONSE_HEADER)

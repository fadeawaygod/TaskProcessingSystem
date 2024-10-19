"""
Definition of the health check for the api service.

Description:
Endpoint for health check by monitor.
"""

from fastapi import APIRouter, status

router: APIRouter = APIRouter()


@router.get("", tags=["health"], description="health check for api server", status_code=status.HTTP_204_NO_CONTENT)
async def health_check_for_api_server():
    """Health check for api server"""
    return

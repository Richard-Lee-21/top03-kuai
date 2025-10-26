from fastapi import APIRouter

from app.api.api_v1.endpoints import top3, admin

api_router = APIRouter()

# Include all API endpoints
api_router.include_router(top3.router, prefix="/top3", tags=["top3"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
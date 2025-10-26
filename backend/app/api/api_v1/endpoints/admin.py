from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import logging
import bcrypt

from app.core.database import get_db
from app.core.cache import get_redis_client
from app.core.config import settings
from app.schemas.admin import LoginRequest, LoginResponse, SettingsResponse, UpdateSettingsRequest
from app.models.configuration import Configuration
from app.utils.auth import verify_admin_password, create_access_token

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
async def admin_login(request: LoginRequest):
    """
    Admin login endpoint
    """
    try:
        if verify_admin_password(request.password):
            token = create_access_token({"sub": "admin"})
            return LoginResponse(
                status="success",
                token=token,
                message="Login successful"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password"
            )
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@router.get("/settings", response_model=SettingsResponse)
async def get_settings(
    token: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get all configuration settings
    """
    try:
        # Verify token (simplified - in production use proper JWT validation)
        if token != "valid_token":  # Replace with actual JWT validation
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Get all configurations from database
        result = await db.execute("SELECT key, value, group FROM configuration")
        settings_data = result.fetchall()
        
        settings_list = [
            {
                "key": row[0],
                "value": row[1],
                "group": row[2]
            }
            for row in settings_data
        ]
        
        return SettingsResponse(
            status="success",
            data=settings_list
        )
        
    except Exception as e:
        logger.error(f"Get settings error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve settings"
        )

@router.post("/settings")
async def update_settings(
    request: UpdateSettingsRequest,
    token: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Update configuration settings
    """
    try:
        # Verify token
        if token != "valid_token":  # Replace with actual JWT validation
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Update settings in database
        for setting in request.settings:
            await db.execute(
                """
                INSERT INTO configuration (key, value, group) 
                VALUES (:key, :value, :group)
                ON CONFLICT (key) 
                DO UPDATE SET value = :value, updated_at = NOW()
                """,
                {
                    "key": setting.key,
                    "value": setting.value,
                    "group": setting.group
                }
            )
        
        # Clear cache to force reload of configuration
        cache_client = get_redis_client()
        await cache_client.flushdb()
        
        return {
            "status": "success",
            "message": "Settings updated successfully"
        }
        
    except Exception as e:
        logger.error(f"Update settings error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update settings"
        )
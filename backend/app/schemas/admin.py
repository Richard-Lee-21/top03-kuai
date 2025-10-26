from pydantic import BaseModel, Field
from typing import List, Optional

class LoginRequest(BaseModel):
    """
    Admin login request schema
    """
    password: str = Field(..., min_length=1, description="Admin password")

class LoginResponse(BaseModel):
    """
    Admin login response schema
    """
    status: str = Field(..., description="Response status")
    token: str = Field(..., description="Authentication token")
    message: str = Field(..., description="Response message")

class SettingItem(BaseModel):
    """
    Individual setting item schema
    """
    key: str = Field(..., description="Configuration key")
    value: Optional[str] = Field(None, description="Configuration value")
    group: Optional[str] = Field(None, description="Group for admin UI organization")

class SettingsResponse(BaseModel):
    """
    Settings response schema
    """
    status: str = Field(..., description="Response status")
    data: List[SettingItem] = Field(..., description="List of configuration settings")

class UpdateSettingItem(BaseModel):
    """
    Setting item for update request
    """
    key: str = Field(..., description="Configuration key")
    value: str = Field(..., description="Configuration value")
    group: str = Field(..., description="Group for organization")

class UpdateSettingsRequest(BaseModel):
    """
    Update settings request schema
    """
    settings: List[UpdateSettingItem] = Field(..., description="List of settings to update")

class AdminResponse(BaseModel):
    """
    Generic admin response schema
    """
    status: str = Field(..., description="Response status")
    message: str = Field(..., description="Response message")
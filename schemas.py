from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Any, Dict


class TokenRequest(BaseModel):
    provider: str
    code: str
    redirect_uri: HttpUrl


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = "Bearer"


class ToolRequest(BaseModel):
    provider: str
    tool: str
    parameters: Dict[str, Any] = {}


class ToolResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None


class AuthStatus(BaseModel):
    provider: str
    connected: bool
    user: Optional[str] = None

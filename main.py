from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import HttpUrl
from typing import Optional
import secrets

from config import settings
from schemas import TokenRequest, TokenResponse, ToolRequest, ToolResponse, AuthStatus
from auth.oauth import build_auth_url, exchange_code, refresh_token
from auth.token_store import token_store
from integrations import get_tool

app = FastAPI(title="ComposioFREE", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/auth/{provider}/url")
def auth_url(provider: str, redirect_uri: HttpUrl):
    state = secrets.token_urlsafe(16)
    url = build_auth_url(provider, state, str(redirect_uri))
    return {"url": url, "state": state}


@app.post("/auth/{provider}/callback", response_model=TokenResponse)
async def auth_callback(provider: str, payload: TokenRequest):
    if provider not in {"google", "github", "slack", "discord"}:
        raise HTTPException(status_code=400, detail="Unsupported provider")
    try:
        tokens = await exchange_code(provider, payload.code, str(payload.redirect_uri))
        token_store.save("default_user", provider, tokens)
        return TokenResponse(
            access_token=tokens.get("access_token", ""),
            refresh_token=tokens.get("refresh_token"),
            expires_in=tokens.get("expires_in"),
            token_type=tokens.get("token_type", "Bearer"),
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/tools/invoke", response_model=ToolResponse)
async def invoke_tool(payload: ToolRequest):
    key = f"{payload.provider}.{payload.tool}"
    try:
        tool = get_tool(key)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Tool not found: {key}")
    try:
        result = await tool.execute(payload.parameters)
        return ToolResponse(success=True, data=result)
    except Exception as exc:
        return ToolResponse(success=False, error=str(exc))


@app.get("/auth/status", response_model=AuthStatus)
def auth_status(provider: str):
    record = token_store.get("default_user", provider)
    connected = record is not None
    return AuthStatus(provider=provider, connected=connected)

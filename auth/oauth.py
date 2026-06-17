import httpx
from auth.token_store import token_store
from config import settings


PROVIDER_CONFIG = {
    "google": {
        "auth_url": "https://accounts.google.com/o/oauth2/v2/auth",
        "token_url": "https://oauth2.googleapis.com/token",
        "scopes": ["openid", "email", "profile"],
    },
    "github": {
        "auth_url": "https://github.com/login/oauth/authorize",
        "token_url": "https://github.com/login/oauth/access_token",
        "scopes": ["repo", "user"],
    },
    "slack": {
        "auth_url": "https://slack.com/oauth/v2/authorize",
        "token_url": "https://slack.com/api/oauth.v2.access",
        "scopes": ["chat:write", "users:read"],
    },
    "discord": {
        "auth_url": "https://discord.com/api/oauth2/authorize",
        "token_url": "https://discord.com/api/oauth2/token",
        "scopes": ["identify", "guilds", "messages.read"],
    },
}


def build_auth_url(provider: str, state: str, redirect_uri: str) -> str:
    cfg = PROVIDER_CONFIG.get(provider)
    if not cfg:
        raise ValueError(f"Unsupported provider: {provider}")
    params = {
        "client_id": getattr(settings, f"{provider.upper()}_CLIENT_ID"),
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(cfg["scopes"]),
        "state": state,
        "access_type": "offline",
        "prompt": "consent",
    }
    url = cfg["auth_url"]
    query = "&".join(f"{k}={httpx.QueryParams({k:v})[k]}" for k,v in params.items())
    return f"{url}?{query}"


async def exchange_code(provider: str, code: str, redirect_uri: str) -> Dict[str, Any]:
    cfg = PROVIDER_CONFIG.get(provider)
    if not cfg:
        raise ValueError(f"Unsupported provider: {provider}")
    payload = {
        "client_id": getattr(settings, f"{provider.upper()}_CLIENT_ID"),
        "client_secret": getattr(settings, f"{provider.upper()}_CLIENT_SECRET"),
        "code": code,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    headers = {"Accept": "application/json"}
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.post(cfg["token_url"], data=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()


async def refresh_token(provider: str, refresh_token: str) -> Dict[str, Any]:
    cfg = PROVIDER_CONFIG.get(provider)
    if not cfg:
        raise ValueError(f"Unsupported provider: {provider}")
    payload = {
        "client_id": getattr(settings, f"{provider.upper()}_CLIENT_ID"),
        "client_secret": getattr(settings, f"{provider.upper()}_CLIENT_SECRET"),
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }
    headers = {"Accept": "application/json"}
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.post(cfg["token_url"], data=payload, headers=headers)
        resp.raise_for_status()
        return resp.json()

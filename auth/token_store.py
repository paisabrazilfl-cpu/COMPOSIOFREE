import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet


class TokenStore:
    def __init__(self, storage_path: str = "./data/tokens.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self._key = self._load_or_create_key()
        self._fernet = Fernet(self._key)

    def _key_file(self) -> Path:
        return self.storage_path.parent / ".key"

    def _load_or_create_key(self) -> bytes:
        key_file = self._key_file()
        if key_file.exists():
            return key_file.read_bytes()
        key = Fernet.generate_key()
        key_file.write_bytes(key)
        return key

    def _load(self) -> Dict[str, Any]:
        if not self.storage_path.exists():
            return {}
        try:
            data = self._fernet.decrypt(self.storage_path.read_bytes())
            return json.loads(data)
        except Exception:
            return {}

    def _save(self, data: Dict[str, Any]) -> None:
        payload = json.dumps(data).encode()
        self.storage_path.write_bytes(self._fernet.encrypt(payload))

    def save(self, user_id: str, provider: str, tokens: Dict[str, Any]) -> None:
        data = self._load()
        data.setdefault(user_id, {})[provider] = {
            "tokens": tokens,
            "updated_at": datetime.utcnow().isoformat(),
        }
        self._save(data)

    def get(self, user_id: str, provider: str) -> Optional[Dict[str, Any]]:
        data = self._load()
        return data.get(user_id, {}).get(provider)

    def delete(self, user_id: str, provider: str) -> None:
        data = self._load()
        if user_id in data and provider in data[user_id]:
            del data[user_id][provider]
            self._save(data)

    def is_expired(self, record: Dict[str, Any]) -> bool:
        tokens = record.get("tokens", {})
        expires_in = tokens.get("expires_in")
        updated_at = datetime.fromisoformat(record.get("updated_at", datetime.utcnow().isoformat()))
        if not expires_in:
            return False
        return datetime.utcnow() > updated_at + timedelta(seconds=int(expires_in))


token_store = TokenStore()

from datetime import datetime, timedelta, timezone
import jwt
from .config import config

# 🔥 microservicios registrados
clients_db = {
    "service-a": {"secret": "secret-a", "scope": "orders:read"},
    "service-b": {"secret": "secret-b", "scope": "orders:write"},
}

def authenticate_client(client_id: str, client_secret: str):
    client = clients_db.get(client_id)
    if not client or client["secret"] != client_secret:
        return None
    return client

def create_access_token(client_id: str, audience: str, scope: str):
    now = datetime.now(timezone.utc)
    exp = now + timedelta(seconds=config.ACCESS_TOKEN_EXPIRE_SECONDS)

    payload = {
        "sub": client_id,
        "aud": audience,
        "scope": scope,
        "iat": now,
        "exp": exp,
    }

    return jwt.encode(payload, config.SECRET_KEY, algorithm=config.ALGORITHM)
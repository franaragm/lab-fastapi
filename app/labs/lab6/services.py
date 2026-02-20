from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt

from .config import config

# ---------------------------
# Hashing seguro: Argon2 (sin límite de 72 bytes)
# ---------------------------
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hashea cualquier contraseña usando Argon2.
    """
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifica una contraseña contra su hash.
    """
    return pwd_context.verify(password, hashed_password)

# ---------------------------
# "Base de datos" simulada de microservicios
# ---------------------------
fake_clients_db = {
    "service-a": {
        "username": "service-a",
        "hashed_password": hash_password("secret-a")
    },
    "service-b": {
        "username": "service-b",
        "hashed_password": hash_password("secret-b")
    }
}

# ---------------------------
# Funciones de autenticación
# ---------------------------
def authenticate_client(username: str, password: str) -> dict | None:
    """
    Verifica que un cliente exista y que la contraseña sea correcta.
    Devuelve el usuario si es válido, None si no.
    """
    user = fake_clients_db.get(username)
    if user and verify_password(password, user["hashed_password"]):
        return user
    return None

def create_access_token(username: str) -> str:
    """
    Crea un JWT seguro con payload estándar.
    Incluye:
    - sub: identidad del cliente
    - iat: issued at (timezone-aware UTC)
    - exp: expiración
    - scope: opcional para control de permisos
    """
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": username,
        "iat": now,
        "exp": expire,
        "scope": "service"
    }

    token = jwt.encode(payload, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return token
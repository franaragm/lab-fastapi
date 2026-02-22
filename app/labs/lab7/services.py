"""
services.py

Servicios de autenticación para comunicación segura entre microservicios.

Incluye:
- Autenticación de clientes (OAuth2 client/password style)
- Generación de access tokens JWT de corta duración
- Generación de refresh tokens JWT con rotación
- Verificación segura de refresh tokens

Diseñado para:
✔ Microservicios FastAPI
✔ Comunicación backend ↔ backend
✔ Cookies HttpOnly o Authorization header
✔ Windows (Argon2, sin bcrypt)
"""

from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
from .config import config


# =========================
# Password hashing (Argon2)
# =========================
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# =========================
# Fake DB (ejemplo)
# En producción → PostgreSQL / Redis / Vault
# =========================
fake_clients_db = {
    "service-a": {
        "username": "service-a",
        "hashed_password": pwd_context.hash("secret-a"),
    },
}


# =========================
# Refresh token store
# En producción → Redis (muy importante)
# =========================
refresh_tokens_store = {}  # {username: refresh_token}


# =========================
# Authentication
# =========================
def authenticate_client(username: str, password: str) -> dict | None:
    """
    Verifica las credenciales de un microservicio.

    Args:
        username: Identificador del servicio
        password: Secreto del servicio

    Returns:
        dict | None:
            - Datos del cliente si la autenticación es válida
            - None si las credenciales son incorrectas

    Security:
        ✔ Usa Argon2 para verificación segura
        ✔ Protege contra timing attacks mediante passlib
    """
    user = fake_clients_db.get(username)

    if user and pwd_context.verify(password, user["hashed_password"]):
        return user

    return None


# =========================
# Access Token
# =========================
def create_access_token(username: str) -> str:
    """
    Genera un JWT access token de corta duración.

    El access token se usa para:
    - Autorización entre microservicios
    - Acceso a endpoints protegidos

    Args:
        username: Servicio autenticado

    Returns:
        str: JWT firmado

    Security:
        ✔ Token corto (reduce impacto si se filtra)
        ✔ Incluye scope para autorización granular
        ✔ Timezone-aware (evita warnings futuros de Python)
    """
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": username,
        "iat": now,
        "exp": expire,
        "scope": "service",
    }

    return jwt.encode(payload, config.SECRET_KEY, algorithm=config.ALGORITHM)


# =========================
# Refresh Token (rotación)
# =========================
def create_refresh_token(username: str) -> str:
    """
    Genera un refresh token JWT con rotación.

    Características:
    - Larga duración
    - Almacena el token activo
    - Invalida automáticamente el anterior

    Args:
        username: Servicio autenticado

    Returns:
        str: Refresh token JWT

    Security:
        ✔ Rotación automática (protección contra replay attack)
        ✔ Diseñado para cookies HttpOnly
        ✔ Debe almacenarse en Redis en producción
    """
    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=config.REFRESH_TOKEN_EXPIRE_DAYS)

    payload = {
        "sub": username,
        "iat": now,
        "exp": expire,
    }

    token = jwt.encode(payload, config.SECRET_KEY, algorithm=config.ALGORITHM)

    # Rotación: invalida refresh anterior
    refresh_tokens_store[username] = token

    return token


# =========================
# Refresh verification
# =========================
def verify_refresh_token(token: str) -> str | None:
    """
    Verifica un refresh token y valida la rotación.

    Args:
        token: Refresh token recibido (cookie o body)

    Returns:
        str | None:
            - Username si el token es válido
            - None si el token es inválido, expirado o reutilizado

    Security:
        ✔ Detecta refresh token reutilizado
        ✔ Previene token replay
        ✔ Firma y expiración verificadas
    """
    try:
        payload = jwt.decode(
            token,
            config.SECRET_KEY,
            algorithms=[config.ALGORITHM],
        )

        username = payload.get("sub")

        # Verifica rotación
        if not username or refresh_tokens_store.get(username) != token:
            return None

        return username

    except jwt.PyJWTError:
        return None
"""
dependencies.py

Dependencias de seguridad reutilizables para FastAPI.

Incluye:
- Verificación de access token JWT desde Authorization header (Bearer)
- Extracción segura de refresh token desde cookies HttpOnly

Diseñado para:
✔ Endpoints protegidos entre microservicios
✔ APIs con cookies seguras
✔ Arquitectura Zero-Trust backend ↔ backend
"""

from fastapi import Security, HTTPException, status, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from .config import config


# =========================
# Bearer scheme (Authorization header)
# =========================
bearer_scheme = HTTPBearer()


def verify_access_token(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
) -> str:
    """
    Verifica y decodifica el access token JWT enviado en el Authorization header.

    Espera el formato:
        Authorization: Bearer <access_token>

    Args:
        credentials: Credenciales extraídas automáticamente por FastAPI

    Returns:
        str: Username (subject) contenido en el JWT

    Raises:
        HTTPException(401):
            - Token inválido
            - Token expirado
            - Payload malformado

    Security:
        ✔ Verifica firma JWT
        ✔ Valida expiración automáticamente
        ✔ Diseñado para comunicación microservicio ↔ microservicio
        ✔ Compatible con Swagger Authorize
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            config.SECRET_KEY,
            algorithms=[config.ALGORITHM],
        )

        username = payload.get("sub")

        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
            )

        return username

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )


def get_refresh_token(refresh_token: str | None = Cookie(default=None)) -> str:
    """
    Extrae el refresh token desde una cookie HttpOnly.

    Esta dependencia permite implementar:
    - Rotación de refresh tokens
    - Renovación silenciosa de sesión
    - Seguridad contra XSS (cookie no accesible por JS)

    Args:
        refresh_token: Cookie HttpOnly enviada automáticamente por el navegador

    Returns:
        str: Refresh token JWT

    Raises:
        HTTPException(401): Si la cookie no está presente

    Security:
        ✔ Cookie HttpOnly (protección XSS)
        ✔ Puede combinarse con SameSite + Secure
        ✔ Ideal para login web y paneles internos
    """
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token faltante",
        )

    return refresh_token
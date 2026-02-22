"""
router.py

Rutas de autenticación avanzada para Lab7.

Incluye:
✔ Login con emisión de access + refresh token
✔ Refresh token con rotación segura
✔ Endpoint protegido con JWT

Diseñado para:
- Arquitecturas Zero-Trust
- Comunicación segura entre microservicios
- Aplicaciones web con cookies HttpOnly
"""

from fastapi import APIRouter, Depends, Response, HTTPException, status
from .schemas import TokenResponse, UserCredentials
from .services import (
    authenticate_client,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
)
from .dependencies import verify_access_token, get_refresh_token

router = APIRouter(prefix="/lab7", tags=["Lab7 - Auth avanzada"])


# =========================
# LOGIN
# =========================
@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login y emisión de tokens",
    description="Autentica el cliente y emite access token JWT + refresh token en cookie HttpOnly.",
)
def login(credentials: UserCredentials, response: Response):
    """
    Autentica un cliente mediante username/password.

    Flujo:
    1. Verifica credenciales
    2. Genera access token (corto plazo)
    3. Genera refresh token (largo plazo)
    4. Guarda refresh en cookie HttpOnly

    Security:
        ✔ Refresh protegido contra XSS
        ✔ Separación access vs refresh
        ✔ Compatible con APIs internas y paneles web
    """
    user = authenticate_client(credentials.username, credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )

    access = create_access_token(user["username"])
    refresh = create_refresh_token(user["username"])

    response.set_cookie(
        key="refresh_token",
        value=refresh,
        httponly=True,
        secure=False,  # ⚠️ True en producción
        samesite="Lax",
        max_age=7 * 24 * 3600,
    )

    return TokenResponse(
        access_token=access,
        token_type="bearer",
        expires_in=5 * 60,
    )


# =========================
# REFRESH
# =========================
@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Rotación de refresh token",
    description="Genera un nuevo access token y rota el refresh token usando cookie HttpOnly.",
)
def refresh(response: Response, refresh_token: str = Depends(get_refresh_token)):
    """
    Renueva la sesión usando refresh token.

    Flujo:
    1. Lee refresh token desde cookie
    2. Valida firma y rotación
    3. Emite nuevo access token
    4. Rota refresh token y sobrescribe cookie

    Security:
        ✔ Refresh rotation (anti replay attack)
        ✔ Sesiones largas seguras
        ✔ Patrón usado en sistemas bancarios y SaaS
    """
    username = verify_refresh_token(refresh_token)

    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido",
        )

    new_access = create_access_token(username)
    new_refresh = create_refresh_token(username)

    response.set_cookie(
        key="refresh_token",
        value=new_refresh,
        httponly=True,
        secure=False,  # True en prod
        samesite="Lax",
        max_age=7 * 24 * 3600,
    )

    return TokenResponse(
        access_token=new_access,
        token_type="bearer",
        expires_in=5 * 60,
    )


# =========================
# PROTECTED
# =========================
@router.get(
    "/protected",
    summary="Endpoint protegido",
    description="Ejemplo de endpoint protegido que requiere access token JWT en Authorization header.",
)
def protected(current: str = Depends(verify_access_token)):
    """
    Endpoint protegido mediante access token.

    Requiere:
        Authorization: Bearer <access_token>

    Uso:
        ✔ Comunicación backend ↔ backend
        ✔ APIs internas
        ✔ Gateways Zero-Trust
    """
    return {"message": f"Hola {current}, acceso seguro"}
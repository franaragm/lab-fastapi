from fastapi import Header, Depends, Request, HTTPException
from .services import UserService

# 🔹 Extrae token del header
def get_token(
    x_token: str = Header(..., description="Token de autenticación")
) -> str:
    """
    Extrae token de la cabecera.
    """
    return x_token

# 🔹 Factory de UserService
def get_user_service() -> UserService:
    """
    Retorna una instancia de UserService.
    """
    return UserService()

# 🔹 Obtiene usuario válido usando token
def get_current_user(
    token: str = Depends(get_token),
    service: UserService = Depends(get_user_service)
) -> dict:
    """
    Valida token y retorna usuario.
    """
    return service.get_user_by_token(token)

# 🔹 Dependency GLOBAL que bloquea acceso si token inválido
def require_valid_token(
    current_user: dict = Depends(get_current_user)
):
    """
    Se ejecuta antes de cada endpoint para validar token.
    """
    # current_user ya lanza excepción si token inválido
    # aquí simplemente pasamos para poder usar en endpoints opcionalmente
    return current_user

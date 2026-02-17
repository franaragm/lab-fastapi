from fastapi import Depends, Header
from .services import ConfigService

def get_api_key(
    api_key: str = Header(..., description="API Key de autenticación")
) -> str:
    """
    Dependency para extraer API Key del header.
    """
    return api_key


def get_config_service(
    api_key: str = Depends(get_api_key)
) -> ConfigService:
    """
    Factory del ConfigService.
    Permite escalar luego (DB, cache, etc).
    """
    return ConfigService(api_key=api_key)

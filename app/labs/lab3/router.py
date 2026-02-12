from typing import Annotated
from fastapi import APIRouter, Depends

from .services import ConfigService
from .dependencies import get_config_service

router = APIRouter(
    prefix="/lab3",
    tags=["Lab3 - servicios inyectados"]
)

# Dependency tipada reutilizable
ConfigServiceDep = Annotated[
    ConfigService,
    Depends(get_config_service)
]


@router.get("/limit")
def obtener_limite(
    service: ConfigServiceDep
):
    """
    Obtiene límite de requests si API Key es válida.
    """

    # Validación centralizada en service
    service.check_permision()

    return {
        "limite": service.get_limit()
    }

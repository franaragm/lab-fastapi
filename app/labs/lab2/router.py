from typing import Annotated
from fastapi import APIRouter, Depends

from .schemas import P2Response, P2Request
from .services import UserService
from .dependencies import get_user_service

router = APIRouter(
    prefix="/lab2",
    tags=["Lab2 - servicios inyectados"]
)

# 🔥 Dependency tipada reutilizable
UserServiceDep = Annotated[
    UserService,
    Depends(get_user_service)  # Factory explícita (mejor que Depends())
]

@router.get(
    "/usuarios/{user_id}",
    response_model=P2Response
)
def get_user(
    user_id: int,
    service: UserServiceDep
):
    """
    Endpoint: Obtener usuario por ID.
    FastAPI inyecta automáticamente UserService.
    """

    return service.get_user(user_id)


@router.post(
    "/usuarios",
    response_model=P2Response
)
def create_user(
    req: P2Request,
    service: UserServiceDep
):
    """
    Endpoint: Crear usuario.
    """

    return service.create_user(req.name, req.email)

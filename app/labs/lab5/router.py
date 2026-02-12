from typing import Annotated
from fastapi import APIRouter, Depends
from .dependencies import require_valid_token

router = APIRouter(
    prefix="/lab5",
    tags=["Lab5 - nested dependencies global token"],
    
    # 🔥 Dependency global que valida token en todas las rutas
    dependencies=[Depends(require_valid_token)]
)


@router.get("/me")
def read_me():
    """
    Endpoint que retorna datos del usuario actual.
    No es necesario poner Depends en cada endpoint, token ya validado globalmente.
    """
    return {"message": "Access granted!"}


@router.get("/dashboard")
def dashboard():
    """
    Otra ruta que requiere token válido.
    """
    return {"message": "Welcome to the dashboard!"}

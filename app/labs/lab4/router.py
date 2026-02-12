from fastapi import APIRouter, Depends
from .dependencies import audit_dependency

router = APIRouter(
    prefix="/lab4",
    tags=["Lab4 - servicios inyectados globalmente"],
    
    # 🔥 Dependency GLOBAL para todas las rutas
    dependencies=[Depends(audit_dependency)]
)


@router.get("/products")
def get_products():
    """
    No recibe service.
    Pero audit_dependency se ejecuta igual.
    """
    return ["Laptop", "Mouse", "Teclado"]


@router.get("/orders")
def get_orders():
    return [
        {"id": 1, "total": 150},
        {"id": 2, "total": 300}
    ]

from fastapi import Depends, Header, Request, HTTPException
from .services import AuditService


def get_client_id(
    x_client_id: str = Header(..., description="ID del cliente")
) -> str:
    """
    Extrae Client ID del header.
    """
    return x_client_id


def get_audit_service(
    client_id: str = Depends(get_client_id)
) -> AuditService:
    """
    Factory AuditService.
    """
    return AuditService(client_id)


def audit_dependency(
    request: Request,
    service: AuditService = Depends(get_audit_service)
):
    """
    🔥 Dependency GLOBAL
    Se ejecuta en TODAS las rutas del router.
    """

    # Ejemplo validación global
    if service.client_id == "blocked-client":
        raise HTTPException(
            status_code=403,
            detail="Cliente bloqueado"
        )

    # Auditoría global
    service.register_access(str(request.url))

from fastapi import APIRouter, HTTPException, Depends
from .schemas import ClientCredentials, TokenResponse
from .services import authenticate_client, create_access_token
from .dependencies import verify_service_token
from .config import config

router = APIRouter(prefix="/lab8", tags=["Lab8 - Microservices"])

# 🔐 AUTH SERVER
@router.post("/token", response_model=TokenResponse, summary="Emitir token M2M")
def issue_token(data: ClientCredentials):
    client = authenticate_client(data.client_id, data.client_secret)
    if not client:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = create_access_token(data.client_id, data.audience, client["scope"])

    return TokenResponse(access_token=token, expires_in=config.ACCESS_TOKEN_EXPIRE_SECONDS)


# 🛡 SERVICE B
@router.get("/service-b/orders", summary="Endpoint protegido Service B")
def get_orders(payload: dict = Depends(verify_service_token)):
    return {
        "service": "service-b",
        "caller": payload["sub"],
        "scope": payload["scope"],
        "message": "Orders secure data"
    }
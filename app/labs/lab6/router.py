from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .schemas import TokenResponse, UserCredentials
from .services import authenticate_client, create_access_token
from .dependencies import verify_token

router = APIRouter(
    prefix="/lab6",
    tags=["Lab6 - Rutas con autenticación"]
)

# Esquema para Swagger/OpenAPI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/lab6/login")

# ---------------------------
# LOGIN → Genera JWT desde JSON
# ---------------------------
@router.post("/login", response_model=TokenResponse)
def login(credentials: UserCredentials):
    user = authenticate_client(credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña inválidos"
        )
    token = create_access_token(user["username"])
    return TokenResponse(access_token=token, token_type="bearer", expires_in=5*60)

# ---------------------------
# RUTA PROTEGIDA con Swagger
# ---------------------------
@router.get("/protected")
def protected_route(current_client: str = Depends(verify_token)):
    """
    Ruta protegida: Swagger mostrará el botón "Authorize" para poner el JWT.
    """
    return {"message": f"Hola {current_client}, tienes acceso a esta ruta segura"}
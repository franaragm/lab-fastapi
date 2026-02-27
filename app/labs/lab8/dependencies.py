from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from .config import config

bearer = HTTPBearer()

def verify_service_token(
    credentials: HTTPAuthorizationCredentials = Security(bearer),
    expected_audience: str = "service-b",
):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            config.SECRET_KEY,
            algorithms=[config.ALGORITHM],
            audience=expected_audience,
        )
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
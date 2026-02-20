from pydantic import BaseModel, Field

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class UserCredentials(BaseModel):
    username: str = Field(..., description="Nombre de usuario o cliente", example="service-a")
    password: str = Field(..., description="Contraseña del cliente", example="secret-a")
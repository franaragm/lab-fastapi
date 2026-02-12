from pydantic import BaseModel, Field

class P2Request(BaseModel):
    # Modelo de entrada para crear usuario
    name: str = Field(..., description="nombre de usuario", example="Fran")
    email: str = Field(..., description="email de usuario", example="francisco.aragon@example.com")


class P2Response(BaseModel):
    # Modelo de salida (lo que devuelve la API)
    id: int = Field(..., description="id de usuario")
    name: str = Field(..., description="nombre de usuario")
    email: str = Field(..., description="email de usuario", example="francisco.aragon@example.com")

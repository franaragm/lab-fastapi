from pydantic import BaseModel, Field

class ClientCredentials(BaseModel):
    client_id: str = Field(example="service-a")
    client_secret: str = Field(example="secret-a")
    audience: str = Field(example="service-b")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
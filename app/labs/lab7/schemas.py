from pydantic import BaseModel, Field

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class UserCredentials(BaseModel):
    username: str = Field(..., example="service-a")
    password: str = Field(..., example="secret-a")
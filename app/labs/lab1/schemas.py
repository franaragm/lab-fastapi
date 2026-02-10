from pydantic import BaseModel, Field, HttpUrl

class P1Request(BaseModel):
    message: str = Field(..., example="Crea una tarea llamada Preparar informe para mañana")

class P1Response(BaseModel):
    action: str = Field(..., description="Tipo de acción que el usuario quiere realizar")
    title: str | None = Field(None, description="Título si aplica (por ejemplo crear tarea)")
    due_date: str | None = Field(None, description="Fecha en formato YYYY-MM-DD si aplica")
    
class PostResponse1(BaseModel):
    userId: int
    id: int
    title: str
    body: str
    
class RepoRequest(BaseModel):
    url: HttpUrl = Field(..., example="https://api.github.com/repos/franaragm/lab-fastapi")

class RepoResponse(BaseModel):
    name: str
    stars: int
    lang: str
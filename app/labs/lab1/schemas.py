from pydantic import BaseModel, Field

class P1Request(BaseModel):
    message: str = Field(..., example="Crea una tarea llamada Preparar informe para mañana")

class P1Response(BaseModel):
    action: str = Field(..., description="Tipo de acción que el usuario quiere realizar")
    title: str | None = Field(None, description="Título si aplica (por ejemplo crear tarea)")
    due_date: str | None = Field(None, description="Fecha en formato YYYY-MM-DD si aplica")

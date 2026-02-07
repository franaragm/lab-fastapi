from fastapi import APIRouter
from .llm_client import llm_chain_google

from .labs.lab1.router import router as lab1_router

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/test-llm-google")
def test_llm_google():
    llm = llm_chain_google()
    answer = llm.invoke("Dime una frase corta para confirmar conexión.")
    return {"response": answer.content}

# --- Proyectos Laboratorio ---
router.include_router(lab1_router)
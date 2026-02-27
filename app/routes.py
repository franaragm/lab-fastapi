from fastapi import APIRouter
from .llm_client import llm_chain_google

from .labs.lab1.router import router as lab1_router
from .labs.lab2.router import router as lab2_router
from .labs.lab3.router import router as lab3_router
from .labs.lab4.router import router as lab4_router
from .labs.lab5.router import router as lab5_router
from .labs.lab6.router import router as lab6_router
from .labs.lab7.router import router as lab7_router
from .labs.lab8.router import router as lab8_router

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/test-llm-google")
async def test_llm_google():
    llm = llm_chain_google()
    answer = await llm.ainvoke("Dime una frase corta para confirmar conexión.")
    return {"response": answer.content}

# --- Proyectos Laboratorio ---
router.include_router(lab1_router)
router.include_router(lab2_router)
router.include_router(lab3_router)
router.include_router(lab4_router)
router.include_router(lab5_router)
router.include_router(lab6_router)
router.include_router(lab7_router)
router.include_router(lab8_router)

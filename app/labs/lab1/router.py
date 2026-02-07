from fastapi import APIRouter
from datetime import date
from app.llm_client import llm_chain_google
from .prompts import intent_prompt
from .schemas import P1Request, P1Response

router = APIRouter(prefix="/p1", tags=["P1 - Prompts & Templates"])

@router.post(
    "/query",
    summary="Analiza la intención del usuario y devuelve un JSON estructurado",
    description="""
    Recibe un mensaje de usuario, lo envía a un modelo de lenguaje para analizar la intención y devuelve un JSON estructurado y validado con Pydantic.
    Se puede usar para crear tareas, actualizar tareas o consultar el estado de tareas.
    Si se indica una fecha relativa, se calcula en base a la fecha actual.
    """,
    response_description="JSON estructurado con la respuesta del asistente",
    response_model=P1Response
)
async def parse_intent(req: P1Request):
    try: 
        today = date.today().strftime("%Y-%m-%d")
        prompt = intent_prompt.format(user_message=req.message, today=today)

        # Inicializar LLM con salida estructurada
        llm = llm_chain_google().with_structured_output(P1Response)

        # Ejecutar modelo
        result: P1Response = llm.invoke(prompt)

        return result
    except Exception as e:
        return {"error": str(e)}
    

@router.post(
    "/query-chain",
    summary="(Version con chains) Analiza la intención del usuario y devuelve un JSON estructurado",
    description="""
    Recibe un mensaje de usuario, lo envía a un modelo de lenguaje para analizar la intención y devuelve un JSON estructurado y validado con Pydantic.
    Se puede usar para crear tareas, actualizar tareas o consultar el estado de tareas.
    Si se indica una fecha relativa, se calcula en base a la fecha actual. Version con chains.
    """,
    response_description="JSON estructurado con la respuesta del asistente",
    response_model=P1Response
)
def parse_intent(req: P1Request):
    try:
        today = date.today().strftime("%Y-%m-%d")
        llm = llm_chain_google().with_structured_output(P1Response)
        chain = intent_prompt | llm
    
        result: P1Response = chain.invoke({"user_message": req.message, "today": today})
        
        return result
    except Exception as e:
        return {"error": str(e)}

    

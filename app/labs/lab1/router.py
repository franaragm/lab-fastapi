from fastapi import APIRouter, HTTPException, BackgroundTasks
import asyncio
import time
import httpx
from datetime import date, datetime
from app.llm_client import llm_chain_google
from .prompts import intent_prompt
from .schemas import P1Request, P1Response, PostResponse1, RepoRequest, RepoResponse
from .utils import extract_owner_repo
from .constants import URL

router = APIRouter(prefix="/p1", tags=["P1 - Prompts & Templates"])

# =============================
# Llamadas a modelos llm
# =============================

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
        result: P1Response = await llm.ainvoke(prompt)

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
async def parse_intent(req: P1Request):
    try:
        today = date.today().strftime("%Y-%m-%d")
        llm = llm_chain_google().with_structured_output(P1Response)
        chain = intent_prompt | llm
    
        result: P1Response = await chain.ainvoke({"user_message": req.message, "today": today})
        
        return result
    except Exception as e:
        return {"error": str(e)}


# =============================
# Llamadas externas asincronas
# llamadas a endpoints externos
# =============================
    
@router.get(
    "/external",
    response_model=PostResponse1,
    summary="Obtiene un post desde JSONPlaceholder"
)
async def get_external_post():
    try:
        # Creamos un cliente HTTP asíncrono con timeout de 10 segundos
        # El "async with" asegura que las conexiones se cierren correctamente
        async with httpx.AsyncClient(timeout=10) as client:
            
            # Realizamos la petición GET de forma NO bloqueante
            # Mientras espera respuesta, el event loop puede atender otras requests
            response = await client.get(URL)

        # Lanza excepción si el status HTTP es 4xx o 5xx
        # Ej: 404, 500, etc.
        response.raise_for_status()

        # Convertimos el JSON de la respuesta a diccionario Python
        data = response.json()

        # Convertimos el dict en un objeto Pydantic validado
        # Si faltan campos o tipos incorrectos → Pydantic lanza error
        return PostResponse1(**data)

    # Captura errores HTTP válidos pero con status error (ej 404, 500)
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,   # Devolvemos el mismo status del servidor remoto
            detail=f"Error remoto: {e.response.text}"
        )
        
    # Captura errores de red: DNS, timeout, conexión rechazada, etc.
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=500,    # Error interno del servidor       
            detail=f"Error de conexión: {str(e)}" # Descripción del error de conexión
        )

# =============================
# Background Tasks
# Tarea que se ejecuta después de responder al usuario
# =============================

# ejemplo 1

async def log_intent_background(message: str, intent: str):
    """
    Guarda un log de la intención detectada en una tarea de fondo.
    
    :param message: El mensaje original del usuario.
    :type message: str
    :param intent: La intención detectada por el modelo de lenguaje.
    :type intent: str
    """
    print(f"[BG] Guardando log de intención...")
    await asyncio.sleep(2)  # Simula guardado lento
    print(f"[BG] Mensaje: {message}")
    print(f"[BG] Intent detectado: {intent}")

@router.post(
    "/query-bg",
    response_model=P1Response,
    summary="Analiza intención y registra log en background"
)
async def parse_intent_background(
    req: P1Request,
    background_tasks: BackgroundTasks
):
    try:
        today = date.today().strftime("%Y-%m-%d")
        prompt = intent_prompt.format(user_message=req.message, today=today)

        llm = llm_chain_google().with_structured_output(P1Response)

        result: P1Response = await llm.ainvoke(prompt)

        # 👇 Tarea background (NO bloquea respuesta)
        background_tasks.add_task(
            log_intent_background,
            req.message,
            result.intent if hasattr(result, "intent") else "unknown"
        )

        return result

    except Exception as e:
        return {"error": str(e)}


# ejemplo 2

async def notify_external_service(intent: str):
    """
    Notifica a un servicio externo sobre la intención detectada.
    
    :param intent: La intención detectada que se enviará al servicio externo. Por ejemplo, "crear_tarea" o "actualizar_tarea".
    :type intent: str 
    """
    try:
        print("[BG] Notificación externa enviada")
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.post(
                "https://jsonplaceholder.typicode.com/posts",
                json={"intent": intent}
            )
            response.raise_for_status() # Raise an exception for bad status codes
            data_from_external_service = response.json()
            print(f"[BG] Respuesta del servicio externo (JSON): {data_from_external_service.get('intent', 'No intent found')}")
    except Exception as e:
        print(f"[BG] Error notificando: {e}")
 
        
@router.post(
    "/query-bg-external", 
    response_model=P1Response,
    summary="Analiza intención y notifica a un servicio externo en background"
)
async def parse_intent_bg_external(
    req: P1Request,
    background_tasks: BackgroundTasks
):
    today = date.today().strftime("%Y-%m-%d")

    llm = llm_chain_google().with_structured_output(P1Response)
    result: P1Response = await llm.ainvoke(
        intent_prompt.format(user_message=req.message, today=today)
    )

    background_tasks.add_task(
        notify_external_service,
        str(result)
    )

    return result

# ejemplo 3

async def analize_repo_details(owner: str, repo: str):
    """
    Analiza información de repositorio y genera un reporte en background.
    """
    print(f"[BG] Iniciando análisis de issues para {owner}/{repo}...")
    try:
        async with httpx.AsyncClient(timeout=30.0) as cliente:
            url_repo = f"https://api.github.com/repos/{owner}/{repo}"
            resp = await cliente.get(url_repo)
            resp.raise_for_status()
            repo_data = resp.json()
            
            total_issues = repo_data.get('open_issues_count', 0)
            description = repo_data.get('description', '')
            visibility = repo_data.get('visibility', '')
            
            reporte = f"""
                REPORTE DE ANÁLISIS
                ===================
                Repositorio: {owner}/{repo}
                Total de issues abiertos: {total_issues}
                Descripción: {description}
                Visibilidad: {visibility}
                Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            print(f"[BG] Análisis completado:\n{reporte}")
    except Exception as e:
        print(f"[BG ERROR] Error al analizar repo: {e}")


@router.post(
    "/github-analyze",
    response_model=RepoResponse,
    summary="Analiza un repositorio de GitHub y genera reporte en background"
)
async def analize_repository_github(
    req: RepoRequest,
    background_tasks: BackgroundTasks
):
    """
    Recibe URL de repositorio y correo, devuelve info básica inmediatamente
    y genera análisis del repo en background.
    """
    try:
        owner, repo = extract_owner_repo(str(req.url))

        async with httpx.AsyncClient(timeout=10.0) as cliente:
            url_api = f"https://api.github.com/repos/{owner}/{repo}"
            resp = await cliente.get(url_api)
            resp.raise_for_status()
            repo_data = resp.json()

        # Programar análisis en background
        background_tasks.add_task(
            analize_repo_details,
            owner,
            repo
        )

        return RepoResponse(
            name=repo_data["full_name"],
            stars=repo_data["stargazers_count"],
            lang=repo_data["language"] or "No especificado"
        )

    except httpx.HTTPStatusError:
        raise HTTPException(status_code=404, detail="Repositorio no encontrado")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="GitHub API no respondió a tiempo")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

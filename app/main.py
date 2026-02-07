from fastapi import FastAPI
from .routes import router
from .utils import get_env

ENV = get_env("ENV", "dev")  # dev | prod

docs_url = "/docs" if ENV == "dev" else None
redoc_url = "/redoc" if ENV == "dev" else None
openapi_url = "/openapi.json" if ENV == "dev" else None

app = FastAPI(
    title="Lab FastAPI",
    description="""
    Laboratorio FastApi para las practicas.
    """,
    version="1.0.0",
    summary="Lab FastAPI",
    docs_url=docs_url,
    redoc_url=redoc_url,
    openapi_url=openapi_url,
)

app.include_router(router)

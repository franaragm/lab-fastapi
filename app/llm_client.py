from langchain_google_genai import ChatGoogleGenerativeAI
from .utils import get_env
from config_base import (
    GOOGLE_LLM_MODEL
)

GOOGLEAI_API_KEY = get_env("GOOGLEAI_API_KEY")

# Devuelve un objeto ChatGoogleGenerativeAI configurado para Google Generative AI. Compatible con LLMChain, RouterChain, MultiPromptChain, agentes, etc.
# ---------- Google ----------
def llm_chain_google(model: str | None = None, temperature: float = 0.7,) -> ChatGoogleGenerativeAI:
    if not GOOGLEAI_API_KEY:
        raise ValueError("GOOGLEAI_API_KEY no está configurada.")
    
    model_to_use = model or GOOGLE_LLM_MODEL

    llm_params = {
        "api_key": GOOGLEAI_API_KEY,
        "temperature": temperature,
    }

    try:
        return ChatGoogleGenerativeAI(model=model_to_use, **llm_params)
    except Exception as e:
        raise RuntimeError(f"No se pudo inicializar el modelo Google '{model_to_use}'.") from e

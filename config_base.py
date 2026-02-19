from pathlib import Path

# ==========================================================
# Configuración base global compartida entre todos los proyectos.
# Define rutas y parámetros comunes para LLM, RAG y almacenamiento.
# ==========================================================

# === Rutas base ===

# Ruta absoluta a la raíz del repositorio
ROOT_DIR = Path(__file__).resolve().parent

# Carpeta de aplicación común (FastAPI, servicios, utilidades)
APP_PATH = ROOT_DIR / "app"

# Parametros para codificar y crear JWT
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# === Configuración LLM ===
GOOGLE_LLM_MODEL = "gemini-2.5-flash"

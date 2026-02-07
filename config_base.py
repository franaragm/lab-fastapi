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

# === Configuración LLM ===
GOOGLE_LLM_MODEL = "gemini-2.5-flash"

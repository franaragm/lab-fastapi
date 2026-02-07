import os
from dotenv import load_dotenv

load_dotenv()  # Carga .env automáticamente

def get_env(name: str, default=None):
    value = os.getenv(name, default)
    if value is None:
        raise ValueError(f"❌ Variable de entorno no encontrada: {name}")
    return value

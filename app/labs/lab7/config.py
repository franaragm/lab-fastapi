import os
from dotenv import load_dotenv

# Cargar variables desde el .env en root
load_dotenv()

class Lab6Config:
    """Configuración centralizada para Lab6"""

    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key")  # fallback dev
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 5))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ["true", "1", "yes"]

    @classmethod
    def validate(cls):
        """Validación de variables críticas"""
        missing_keys = []
        if not cls.SECRET_KEY or cls.SECRET_KEY == "dev-secret-key":
            missing_keys.append("SECRET_KEY")

        if missing_keys:
            raise ValueError(f"Faltan variables críticas: {', '.join(missing_keys)}")

        return True

config = Lab6Config()
config.validate()
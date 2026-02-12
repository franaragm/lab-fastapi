from fastapi import HTTPException

class ConfigService:
    """
    Servicio de lógica de negocio para configuración y permisos.
    """

    def __init__(self, api_key: str):
        # API Key ya validada / obtenida desde dependency
        self.api_key = api_key

        # ⚠️ Demo config
        self.config = {
            "max_requests": 100,
            "timeout": 30
        }

    def get_limit(self) -> int:
        """
        Retorna límite de requests configurado.
        """
        return self.config["max_requests"]

    def validate_api_key(self) -> bool:
        """
        Valida API Key.
        """
        return self.api_key == "clave-secreta"

    def check_permision(self):
        """
        Helper para lanzar excepción si no tiene permiso.
        """
        if not self.validate_api_key():
            raise HTTPException(
                status_code=403,
                detail="API Key inválida"
            )

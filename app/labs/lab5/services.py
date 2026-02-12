from fastapi import HTTPException

class UserService:
    """
    Servicio de lógica de negocio para usuarios.
    """

    # Datos de ejemplo en memoria
    def __init__(self):
        self.users = {
            1: {"id": 1, "name": "Alice", "token": "token-123"},
            2: {"id": 2, "name": "Bob", "token": "token-456"},
        }

    def get_user_by_token(self, token: str) -> dict:
        """
        Busca usuario por token. Lanza error si no existe.
        """
        for user in self.users.values():
            if user["token"] == token:
                return user
        raise HTTPException(status_code=401, detail="Invalid token")

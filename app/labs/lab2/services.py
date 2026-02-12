from fastapi import HTTPException

class UserService:
    """
    Servicio de lógica de negocio.
    En producción normalmente usaría un repository o DB session.
    """

    def __init__(self):
        # ⚠️ Solo demo: memoria local
        # En producción esto vendría de DB
        self.users = {
            1: {"id": 1, "name": "Ana", "email": "ana@example.com"},
            2: {"id": 2, "name": "Luis", "email": "luis@example.com"}
        }

    def get_user(self, user_id: int) -> dict:
        """
        Busca usuario por ID.
        """
        user = self.users.get(user_id)

        if not user:
            # OK para proyectos pequeños
            # En enterprise lanzarías excepción propia
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return user

    def create_user(self, name: str, email: str) -> dict:
        """
        Valida y crea usuario.
        """

        # Validación básica ejemplo
        if "@" not in email:
            raise HTTPException(status_code=400, detail="Email inválido")

        new_id = max(self.users.keys()) + 1

        new_user = {
            "id": new_id,
            "name": name,
            "email": email
        }

        self.users[new_id] = new_user

        return new_user

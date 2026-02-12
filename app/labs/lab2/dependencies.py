from .services import UserService

# permite sub dependencias por ejemplo para que dependa de otro servicio donde se obtiene db
# def get_user_service(db = Depends(get_db)):
#   return UserService(db)

def get_user_service() -> UserService:
    """
    Factory de UserService.

    Ventajas:
    - Permite mock en tests
    - Permite inyectar DB luego
    - Permite config/env
    """
    return UserService()

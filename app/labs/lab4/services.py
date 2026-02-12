
class AuditService:
    """
    Servicio de auditoría.
    Simula registro de accesos.
    """

    def __init__(self, client_id: str):
        self.client_id = client_id

    def register_access(self, url: str):
        """
        Simula guardar log de auditoría.
        """
        print(f"[AUDIT] Cliente={self.client_id} accedió a {url}")

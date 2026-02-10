from urllib.parse import urlparse

def extract_owner_repo(url: str) -> tuple[str, str]:
    """
    Extrae owner y repo de una URL de GitHub.
    Funciona con URLs tipo:
      - https://github.com/owner/repo
      - https://github.com/owner/repo/
      - https://github.com/owner/repo/issues
      - https://api.github.com/repos/owner/repo
      - https://api.github.com/repos/owner/repo/
    
    :param url: URL del repositorio
    :return: tuple(owner, repo)
    :raises ValueError: si no se puede extraer owner y repo
    """
    # Parsear la URL
    parsed = urlparse(url)
    # Tomar la ruta y eliminar / al inicio y final
    path = parsed.path.strip('/')
    # Separar por /
    partes = path.split('/')

    # Buscar patrón: [repos?, owner, repo, ...]
    if len(partes) >= 2:
        # Si es API (ej: /repos/owner/repo), tomar los últimos 2
        owner = partes[-2]
        repo = partes[-1]
        return owner, repo
    else:
        raise ValueError(f"No se pudo extraer owner y repo de la URL: {url}")

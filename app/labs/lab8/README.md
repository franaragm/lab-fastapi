# 🚀 Lab8 — Comunicación segura entre microservicios

## 🎯 Qué implementa

✅ OAuth2 Client Credentials
✅ JWT con **audience validation**
✅ scopes por microservicio
✅ cliente HTTP con **token cache**
✅ sin cookies (solo Authorization header)
✅ listo para migrar a IdP externo

---

# 📁 Estructura

```
lab8/
├── config.py
├── schemas.py
├── services.py
├── dependencies.py
└── router.py          # 👈 Auth + Service B
```

---

# client.py (🔥 Service A con cache de token) Service A simulando llamadas

Se simula comunicacion desde otro servicio con client.py

```python
import time
import requests

TOKEN_CACHE = {"token": None, "exp": 0}

AUTH_URL = "http://localhost:8000/lab8/token"
SERVICE_B_URL = "http://localhost:8000/lab8/service-b/orders"

def get_token():
    if TOKEN_CACHE["token"] and TOKEN_CACHE["exp"] > time.time():
        return TOKEN_CACHE["token"]

    res = requests.post(
        AUTH_URL,
        json={
            "client_id": "service-a",
            "client_secret": "secret-a",
            "audience": "service-b",
        },
    ).json()

    TOKEN_CACHE["token"] = res["access_token"]
    TOKEN_CACHE["exp"] = time.time() + res["expires_in"] - 5
    return TOKEN_CACHE["token"]

def call_service_b():
    token = get_token()

    res = requests.get(
        SERVICE_B_URL,
        headers={"Authorization": f"Bearer {token}"}
    )

    return res.json()
```

---

✅ autenticación entre microservicios
✅ tokens con audience (MUY crítico)
✅ scopes
✅ cache para evitar pedir token siempre
✅ desacoplamiento total

---



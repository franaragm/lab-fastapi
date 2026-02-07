# **Laboratorio FastAPI**

| Tecnología                 | Para qué se usa                         |
| -------------------------- | --------------------------------------- |
| **Python**                 | Lenguaje principal del servidor IA      |
| **FastAPI**                | Crear endpoints HTTP que devuelven JSON |
| **LangChain**              | Orquestación de LLMs, agentes y RAG     |
| **SQLAlchemy / Databases** | Acceso a bases de datos SQL async       |
| **Beanie (MongoDB)**       | ODM async para Mongo + Pydantic         |
| **Passlib + JWT**          | Autenticación segura                    |
| **Pytest**                 | Testing del backend                     |

---

## 🏗️ Estructura del repositorio

```
├── 📁 app
│   ├── 📁 labs
│   │   ├── 📁 lab1
│   │   │   ├── 🐍 prompts.py
│   │   │   ├── 🐍 router.py
│   │   │   └── 🐍 schemas.py
│   │   └── 📁 lab2
│   │       └── ⚙️ .gitkeep
│   ├── 🐍 llm_client.py
│   ├── 🐍 main.py
│   ├── 🐍 routes.py
│   └── 🐍 utils.py
├── ⚙️ .env.example
├── ⚙️ .gitignore
├── 📝 README.md
├── 🐍 config_base.py
├── 📄 requirements.txt        # Dependencias base (directas)
├── 📄 requirements.lock       # Versiones exactas reproducibles
```

---

## 🧩 Filosofía del proyecto

`/app` contiene **todos los componentes base compartidos**:

* Inicialización de **FastAPI**
* Enrutador general del servidor
* Cliente universal para LLM
* Configuración global
* Utilidades de entorno
* Integración DB
* Seguridad / Auth

Cada lab solo añade endpoints mediante:

```python
router.include_router(labX_router)
```

---

## 🐍 Versiones de Python

Probado con:

* ✅ **Python 3.13**
* ✅ **Python 3.12**
* ✅ **Python 3.11**

⚠️ Evitar versiones demasiado nuevas sin testear en producción.

👉 Actualmente el ecosistema principal ya funciona sobre **Pydantic v2**.

---

## ⚙️ Instalación del entorno

---

### 1️⃣ Crear entorno virtual

```bash
python -m venv .venv

# Activar
source .venv/bin/activate      # Mac / Linux
.venv\Scripts\activate         # Windows
```

---

## 📦 Gestión de dependencias

Este proyecto usa:

| Archivo           | Función                                |
| ----------------- | -------------------------------------- |
| requirements.txt  | Dependencias base elegidas manualmente |
| requirements.lock | Versiones exactas reproducibles        |

---

### Instalar dependencias

```bash
pip install -r requirements.lock
```

👉 Recomendado para desarrollo estable.

---

### Instalar solo dependencias base

```bash
pip install -r requirements.txt
```

---

## 🔒 Actualizar lock correctamente (RECOMENDADO)

En lugar de usar `pip freeze`, se recomienda usar **pip-tools**.

### Instalar pip-tools

```bash
pip install pip-tools
```

---

### Generar lock reproducible

```bash
pip-compile requirements.txt --output-file requirements.lock
```

---

### Actualizar dependencias

```bash
pip-compile --upgrade
```

---

### Actualizar solo un paquete

```bash
pip-compile --upgrade-package fastapi
```

---

## 🧠 Por qué no usar pip freeze

`pip freeze` incluye:

* Dependencias transitivas
* Paquetes del entorno
* Librerías no controladas

👉 pip-compile genera builds reproducibles reales.

---

## 🔐 Seguridad incluida

Stack preparado para:

* Hash seguro contraseñas → **passlib[bcrypt]**
* Tokens JWT → **python-jose**
* Validación datos → **Pydantic**

---

## 🗄️ Base de datos

Soporte para:

### SQL

* SQLAlchemy
* Databases (async)

### MongoDB

* Beanie (ODM async + Pydantic)

---

## 🧪 Testing

```bash
pytest
```

---

## 🌍 Variables de entorno

```bash
cp .env.example .env
```

Ejemplo:

```
GOOGLEAI_API_KEY=API_KEY_HERE
ENV=dev
```

API Keys:

[https://aistudio.google.com/api-keys](https://aistudio.google.com/api-keys)

---

## ▶️ Ejecutar servidor

```bash
uvicorn app.main:app --reload --port 8000
```

---

## 📚 Documentación automática

```
http://localhost:8000/docs
```

---

## 🔎 Endpoints base

```
GET /health
GET /test-llm-google
```

---

## 🛠️ Configuración global

Archivo central:

```
/config_base.py
```

Contiene:

* Config global entorno
* Flags dev / prod
* Variables comunes
* Setup clientes externos

---

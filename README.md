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

## 🚀 Instalación y uso

### 🔧 1) Crear entorno virtual y activar entorno virtual

```bash
python -m venv .venv           # crear entorno virtual
source .venv/bin/activate      # iniciar entorno virtual en macOS / Linux
.venv\Scripts\activate         # iniciar entorno virtual en Windows
```

---

### 📦 2) Instalar dependencias en el entorno virtual iniciado

Este proyecto usa:

| Archivo           | Función                                |
| ----------------- | -------------------------------------- |
| requirements.txt  | Dependencias base elegidas manualmente |
| requirements.lock | Versiones exactas reproducibles        |

Hay dos opciones, se recomienda usar `requirements.lock` para asegurar la reproducibilidad del entorno.

```bash
pip install -r requirements.txt   # instalar dependencias principales del proyecto
pip install -r requirements.lock  # instalar dependencias fijadas
```

Para fijar nuevas dependencias, añadir paquete en requeriments.txt:

```bash
pip install -r requirements.txt # Instala las dependencias listadas en requirements.txt (si hay nuevas)
pip freeze > requirements.lock  # Genera un nuevo archivo lock con las dependencias actuales
```

---

### 🔐 3) Configurar variables de entorno

Copiar y renombrar el archivo `.env.example` a `.env`:

```bash
cp .env.example .env
```

Editar `.env` con tus claves:

```
GOOGLEAI_API_KEY=API_KEY_HERE
ENV=dev
```

#### 🔑 Obtener API keys:

* Google AI → [https://aistudio.google.com/api-keys](https://aistudio.google.com/api-keys)

---

### ▶️ 4) Ejecutar servidor en el entorno virtual iniciado

```bash
uvicorn app.main:app --reload --port 8000
```

📚 Documentación automática

```
http://localhost:8000/docs
```

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

# **Laboratorio Fastapi**

| Tecnología               | Para qué se usa                                                    |
| ------------------------ | ------------------------------------------------------------------ |
| **Python**               | Lenguaje principal del servidor IA                                 |
| **FastAPI**              | Crear endpoints HTTP que devuelven JSON                            |


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
├── 📄 requirements.lock
└── 📄 requirements.txt
```

### Sobre el directorio `app/`

`/app` contiene **todos los componentes base compartidos**:

* Inicialización de **FastAPI**
* Enrutador general del servidor
* Cliente universal para LLM
* Archivos de configuración global
* Utilidades para cargar variables de entorno

Cada lab solo agrega una nueva ruta o endpoint mediante:

```python
router.include_router(labX_router)
```

---

## 🐍 Requisitos de Python

Este proyecto ha sido desarrollado y probado con las siguientes versiones de Python:

- **Python 3.13.2**: Compatible y probado en **macOS (Apple Silicon)** y **Windows**.
- **Python 3.11**: Recomendado para equipos **Mac con procesador Intel**, donde Python 3.13 puede no estar disponible o no ser estable.

⚠️ **No se recomienda usar Python 3.14 o superior**, ya que algunas librerías clave todavía no son compatibles:

- **Pydantic** (LangChain y ChromaDB dependen de Pydantic V1)
- **ChromaDB**
- **LangChain Core**

## ⚙️ Instalación del entorno

### 1) Crear entorno virtual

```bash
python -m venv .venv # crear entorno virtual

# iniciar entorno virtual
source .venv/bin/activate      # Mac / Linux
.venv\Scripts\activate         # Windows
```

### 2) Instalar dependencias

dos opciones: 
```bash
pip install -r requirements.txt # para instalar dependencias
pip install -r requirements.lock # para instalar mismas versiones de dependencias
```

#### Cuando se añade una nueva dependencia en requeriments.txt

```bash
# Paso 1: instalar / actualizar paquetes desde requirements.txt
pip install -r requirements.txt

# Paso 2: generar/actualizar lock file con las versiones exactas
pip freeze > requirements.lock
```

### 3) Configurar variables de entorno

```bash
cp .env.example .env
```

Edita tu `.env`:

```
GOOGLEAI_API_KEY=API_KEY_HERE
ENV=dev
```

Obtener API keys:
[https://aistudio.google.com/api-keys](https://aistudio.google.com/api-keys)

---

## ▶️ Ejecutar el servidor

```bash
uvicorn app.main:app --reload --port 8000
```

Ruta local del http://localhost:8000 para docs

```
http://localhost:8000/docs
```

Rutas de prueba:

```
GET /health
GET /test-llm-google
```

---


## 🛠️ **config_base.py (configuración global del repositorio)**

Este archivo centraliza la configuración compartida entre todos los labs.

Se encuentra en:

```
/config_base.py
```

---



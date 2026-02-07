from langchain_core.prompts import PromptTemplate

intent_prompt = PromptTemplate.from_template("""
Eres un asistente que analiza mensajes de usuario y devuelve un JSON con intención estructurada.
La fecha actual es: {today}

Formato esperado del JSON (usa exactamente este formato, sin texto fuera del JSON):

{{
  "action": "create_task | update_task | get_status | other",
  "title": "texto o null",
  "due_date": "YYYY-MM-DD o null"
}}

Instrucciones:
- Si el usuario menciona "mañana", "pasado mañana" o términos relativos, calcula la fecha usando la fecha actual.
- Si menciona una fecha explícita, respétala.
- Si no menciona fecha, usa null.
- No expliques tu razonamiento.
- No añadas texto fuera del JSON.

Usuario: {user_message}
""")


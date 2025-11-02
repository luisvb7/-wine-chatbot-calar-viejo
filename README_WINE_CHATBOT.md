# Sommelier Virtual - Chatbot de Recomendación de Vinos

Aplicación web interactiva con Streamlit que utiliza la API de Groq para recomendar vinos personalizados durante una cata virtual.

## Características

- Chatbot conversacional impulsado por IA (Groq API)
- Recomendaciones personalizadas de vinos
- Interfaz amigable con Streamlit
- Consejos de maridaje y notas de cata
- Sistema de preguntas inteligentes para entender preferencias

## Requisitos Previos

- Python 3.8 o superior
- Cuenta en Groq (https://console.groq.com) para obtener API key

## Instalación

1. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

2. **Configurar API key de Groq:**

   Opción A - Crear archivo .env:
   ```bash
   cp .env.example .env
   ```
   Luego edita `.env` y agrega tu API key:
   ```
   GROQ_API_KEY=tu_api_key_real_aqui
   ```

   Opción B - Variable de entorno temporal:
   ```bash
   export GROQ_API_KEY=tu_api_key_real_aqui
   ```

## Uso

Ejecuta la aplicación con:

```bash
streamlit run wine_chatbot_app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## Cómo usar el chatbot

1. Inicia una conversación describiendo tus preferencias
2. Responde las preguntas del sommelier virtual
3. Recibe recomendaciones personalizadas de vinos
4. Aprende sobre maridajes y características de cada vino
5. Usa el botón "Nueva Conversación" para empezar de nuevo

## Ejemplos de preguntas

- "Me gustan los sabores dulces y afrutados"
- "Busco un vino para acompañar pescado"
- "Prefiero vinos tintos con cuerpo"
- "Nunca he probado vino, ¿por dónde empiezo?"
- "¿Qué vino va bien con pasta?"

## Obtener API Key de Groq

1. Visita https://console.groq.com
2. Crea una cuenta o inicia sesión
3. Ve a "API Keys"
4. Genera una nueva API key
5. Copia la key y úsala en tu archivo .env

## Estructura de archivos

```
.
├── wine_chatbot_app.py      # Aplicación principal
├── requirements.txt          # Dependencias
├── .env.example             # Plantilla de configuración
└── README_WINE_CHATBOT.md   # Este archivo
```

## Solución de problemas

**Error: "No se encontró GROQ_API_KEY"**
- Verifica que hayas creado el archivo `.env` con tu API key
- O exporta la variable de entorno antes de ejecutar

**Error de conexión con Groq**
- Verifica tu conexión a internet
- Confirma que tu API key sea válida
- Revisa los límites de uso de tu cuenta Groq

## Modelo utilizado

El chatbot utiliza el modelo `llama-3.3-70b-versatile` de Groq, optimizado para conversaciones naturales y recomendaciones precisas.

## Licencia

Proyecto educativo - Uso libre

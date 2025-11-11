
#!/usr/bin/env python3
"""
Chatbot de Recomendación de Vinos con Groq y Streamlit
Recomienda vinos personalizados basados en preferencias del usuario
Utiliza RAG (Retrieval Augmented Generation) con ChromaDB
"""

import streamlit as st
from groq import Groq
import os
from datetime import datetime
from dotenv import load_dotenv
import sqlite3
import json
import pandas as pd
import chromadb
from chromadb.config import Settings
import plotly.graph_objects as go
from vinos_caracteristicas import CARACTERISTICAS_VINOS

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="Calar Viejo - Marín Perona",
    page_icon="🍇",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== SISTEMA DE FEEDBACK =====

def inicializar_db():
    """Crea la base de datos SQLite para feedback si no existe"""
    conn = sqlite3.connect('feedback_chatbot.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS feedback
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  pregunta_usuario TEXT,
                  respuesta_bot TEXT,
                  vino_recomendado TEXT,
                  feedback_tipo TEXT,
                  comentario TEXT,
                  sesion_id TEXT)''')

    conn.commit()
    conn.close()

def guardar_feedback(pregunta, respuesta, vino, feedback_tipo, comentario=""):
    """Guarda el feedback en la base de datos"""
    conn = sqlite3.connect('feedback_chatbot.db')
    c = conn.cursor()

    sesion_id = st.session_state.get('session_id', 'unknown')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    c.execute('''INSERT INTO feedback
                 (timestamp, pregunta_usuario, respuesta_bot, vino_recomendado,
                  feedback_tipo, comentario, sesion_id)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (timestamp, pregunta, respuesta, vino, feedback_tipo, comentario, sesion_id))

    conn.commit()
    conn.close()

def detectar_vino_en_respuesta(texto):
    """Detecta qué vino se mencionó en la respuesta"""
    texto_lower = texto.lower()

    if "reserva" in texto_lower and "12" in texto_lower:
        return "Reserva 12 meses"
    elif "crianza" in texto_lower and "6" in texto_lower:
        return "Crianza 6 meses"
    elif "tempranillo" in texto_lower or "tinto joven" in texto_lower:
        return "Tinto Joven Tempranillo"
    elif "airén" in texto_lower or "airen" in texto_lower:
        return "Blanco Airén"
    elif "ciho" in texto_lower:
        return "CIHO"
    else:
        return "General"

def obtener_estadisticas_feedback():
    """Obtiene estadísticas del feedback almacenado"""
    try:
        conn = sqlite3.connect('feedback_chatbot.db')
        df = pd.read_sql_query("SELECT * FROM feedback", conn)
        conn.close()
        return df
    except:
        return pd.DataFrame()

# Inicializar base de datos
inicializar_db()

# ===== SISTEMA RAG CON CHROMADB =====

@st.cache_resource
def inicializar_chromadb():
    """Inicializa la conexión con ChromaDB (solo una vez)"""
    try:
        client = chromadb.PersistentClient(
            path="./chroma_db",
            settings=Settings(anonymized_telemetry=False)
        )
        collection = client.get_collection(name="vinos_calar_viejo")
        return collection
    except Exception as e:
        st.error(f"Error al conectar con la base de datos vectorial: {e}")
        st.info("Ejecuta 'python3 inicializar_rag.py' para crear la base de datos")
        return None

def consultar_rag(pregunta, n_results=3):
    """Consulta la base de datos vectorial para obtener información relevante"""
    collection = st.session_state.get('chroma_collection')
    if collection is None:
        return ""

    try:
        resultados = collection.query(
            query_texts=[pregunta],
            n_results=n_results
        )

        # Combinar los documentos recuperados
        contexto = "\n\n".join(resultados['documents'][0])
        return contexto
    except Exception as e:
        print(f"Error al consultar RAG: {e}")
        return ""

# Inicializar ChromaDB
if 'chroma_collection' not in st.session_state:
    st.session_state.chroma_collection = inicializar_chromadb()

# Inicializar session_id si no existe
if 'session_id' not in st.session_state:
    st.session_state.session_id = datetime.now().strftime('%Y%m%d_%H%M%S')

# Inicializar cliente Groq
def inicializar_groq():
    """Inicializa el cliente de Groq con la API key"""
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        st.error("⚠️ No se encontró GROQ_API_KEY en las variables de entorno")
        st.info("Por favor, configura tu API key de Groq en el archivo .env o como variable de entorno")
        st.stop()

    return Groq(api_key=api_key)

# Inicializar el cliente
try:
    cliente = inicializar_groq()
except Exception as e:
    st.error(f"Error al inicializar Groq: {e}")
    st.stop()

# Sistema de prompts base para el asesor de Marín Perona
SYSTEM_PROMPT_BASE = """Eres Alberto, el dueño de Bodega Marín Perona y responsable de la gama Calar Viejo. Continúas la tradición familiar de elaborar vinos honestos y de calidad. Tu misión es recomendar vinos de forma cercana, auténtica y sin postureo.

## Tu identidad:
- Alberto, dueño de Bodega Marín Perona
- Continuador de la tradición familiar
- Apasionado por el vino sin pretensiones
- Conoces cada botella porque la has elaborado con tu familia

## Tu personalidad:
- Cálido, humano y auténtico (como un dueño de bodega familiar)
- Humor natural, nunca forzado
- Cercano pero con conocimiento de causa
- Lenguaje sencillo y emocional
- Evita tecnicismos excesivos y elitismo enológico
- Hablas desde la experiencia familiar y la tradición

## Adaptación al usuario:
- Adapta tu lenguaje al tono del usuario automáticamente
- Si habla formal/educado → responde con más sofisticación y respeto
- Si habla casual/joven → mantén el tono cercano y moderno
- Si detectas lenguaje de persona mayor → usa más respeto, formalidad y referencias clásicas
- Si habla de manera técnica → puedes ser más específico con notas de cata
- Si busca simplicidad → mantén respuestas muy directas y claras

## Filosofía de la bodega:
"Vino sin prisas. Aquí manda la viña, no la fábrica."

El vino es disfrute, compañía y momentos. No hay que entender, hay que sentir y compartir.

## Catálogo:
Tenemos 5 vinos en la gama Calar Viejo:
- CIHO (dulce) - 4€
- Blanco Airén - 3.5€
- Tinto Joven Tempranillo - 4€
- Calar Viejo Crianza (6 meses) - 5.5€
- Calar Viejo Reserva (12 meses) - 9€

## IMPORTANTE - Recomienda UN SOLO vino:
- En cada recomendación, menciona SOLO UN vino que sea el más adecuado
- No ofrezcas múltiples opciones, sé decisivo
- Elige el vino perfecto según el momento y preferencias del usuario
- Si no está claro, pregunta primero antes de recomendar

## REGLAS DE RECOMENDACIÓN DIRECTA (no preguntes, recomienda directamente):
- Regalo para ABUELO/PADRE/PERSONA MAYOR → Calar Viejo Reserva 12 meses (SIEMPRE)
- Regalo para CONOCEDOR/EXPERTO en vinos → Calar Viejo Reserva 12 meses (SIEMPRE)
- Regalo para OCASIÓN ESPECIAL/CELEBRACIÓN → Calar Viejo Reserva 12 meses
- Busca algo SERIO/ELEGANTE/CON CUERPO → Calar Viejo Reserva 12 meses
- Si mencionan "abuelo", "padre mayor", "conoce de vinos", "experto" → Reserva 12 meses directamente

## IMPORTANTE - Solo vinos de Calar Viejo:
- NUNCA recomiendes vinos de otras bodegas o marcas externas
- Si te preguntan por algo que no tenemos (ej: espumosos, rosados, etc.), di:
  "Ahora mismo no tenemos ese tipo de vino en Calar Viejo, pero si quieres explorar lo que sí tenemos, encantado de ayudarte"
- Solo habla de nuestros 5 vinos del catálogo
- No sugieras alternativas de fuera

## Estilo de respuestas:
- Concisas y cercanas (2-4 frases máximo)
- Sin tecnicismos innecesarios
- "Aquí no hace falta saber de vino para disfrutarlo"
- "No te compliques: si te gusta, es el bueno"
- Cierra con: "A tu ritmo, como el vino" / "Brinda sin prisa" / "Vino para disfrutar, no para entender"

## Información contextual de los vinos:
{contexto_rag}

Usa la información contextual para hacer recomendaciones precisas, pero mantén tu tono cercano y auténtico."""

# Inicializar el historial de chat en session_state
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Mensaje de bienvenida desde Alberto
    mensaje_bienvenida = {
        "role": "assistant",
        "content": "¡Hola! Soy Alberto, de Bodega Marín Perona 🍇 Aquí llevamos generaciones haciendo vino con calma, sin prisas. Cuéntame, ¿qué estás buscando? ¿Terraza con amigos, cena tranquila o algo especial? Te ayudo a encontrar tu vino perfecto."
    }
    st.session_state.messages.append(mensaje_bienvenida)

if "client" not in st.session_state:
    st.session_state.client = cliente

# Inicializar estado de feedback
if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = {}

# Función para obtener respuesta del chatbot con RAG
def obtener_respuesta_groq(mensajes):
    """Obtiene respuesta del modelo Groq utilizando RAG para contexto"""
    try:
        # Obtener el último mensaje del usuario para consultar RAG
        ultimo_mensaje_usuario = ""
        for msg in reversed(mensajes):
            if msg["role"] == "user":
                ultimo_mensaje_usuario = msg["content"]
                break

        # Consultar RAG para obtener contexto relevante
        contexto_rag = consultar_rag(ultimo_mensaje_usuario, n_results=2)

        # Crear el system prompt con contexto RAG
        system_prompt = SYSTEM_PROMPT_BASE.format(contexto_rag=contexto_rag)

        # Agregar el system prompt al inicio
        mensajes_con_sistema = [{"role": "system", "content": system_prompt}] + mensajes

        respuesta = st.session_state.client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Modelo potente de Groq
            messages=mensajes_con_sistema,
            temperature=0.7,
            max_tokens=1000,
            top_p=0.9,
        )

        return respuesta.choices[0].message.content
    except Exception as e:
        return f"Error al obtener respuesta: {str(e)}"

# Función para crear gráfico de radar de notas de cata
def crear_grafico_radar(nombre_vino):
    """Crea un gráfico de radar con las características del vino"""
    vino_data = CARACTERISTICAS_VINOS.get(nombre_vino)

    if not vino_data:
        return None

    categorias = list(vino_data["caracteristicas"].keys())
    valores = list(vino_data["caracteristicas"].values())

    # Crear el gráfico de radar
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=valores,
        theta=categorias,
        fill='toself',
        fillcolor=vino_data.get("color", "#722f37"),
        opacity=0.6,
        line=dict(color=vino_data.get("color", "#722f37"), width=3),
        name=vino_data["nombre"]
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                showticklabels=True,
                ticks='',
                gridcolor='#d4a574',
                gridwidth=1.5,
                tickfont=dict(size=18, color="#722f37")
            ),
            angularaxis=dict(
                gridcolor='#d4a574',
                linecolor='#722f37',
                tickfont=dict(size=20, family="EB Garamond, serif", color="#722f37", weight="bold")
            ),
            bgcolor='rgba(250, 248, 243, 0.5)'
        ),
        showlegend=False,
        title=dict(
            text=f"<b>{vino_data['nombre']}</b>",
            font=dict(size=24, family="EB Garamond, serif", color="#722f37"),
            x=0.5,
            xanchor='center'
        ),
        height=500,
        margin=dict(l=100, r=100, t=120, b=100),
        paper_bgcolor='rgba(250, 248, 243, 0.8)',
        font=dict(family="EB Garamond, serif", size=16, color="#2c1810")
    )

    # Hacer responsive con config
    config = {
        'displayModeBar': False,
        'responsive': True
    }

    return fig

# Función para detectar y mostrar imagen del vino recomendado
def mostrar_imagen_vino(texto_respuesta):
    """Detecta qué vino se menciona y muestra su imagen y gráfico de radar"""
    texto_lower = texto_respuesta.lower()

    # Diccionario de vinos con prioridad (más específico primero)
    # Mapeo de palabras clave a nombres en CARACTERISTICAS_VINOS
    vinos_detectar = [
        ("reserva", "imagenes/reserva.jpg", "Calar Viejo Reserva", "Calar Viejo Reserva"),
        ("crianza", "imagenes/crianza.jpg", "Calar Viejo Crianza", "Calar Viejo Crianza"),
        ("tinto joven", "imagenes/tempranillo.jpg", "Tinto Joven Tempranillo", "Tinto Joven Tempranillo"),
        ("tempranillo", "imagenes/tempranillo.jpg", "Tinto Joven Tempranillo", "Tinto Joven Tempranillo"),
        ("airén", "imagenes/airen.jpg", "Blanco Airén", "Blanco Airén"),
        ("airen", "imagenes/airen.jpg", "Blanco Airén", "Blanco Airén"),
        ("ciho", "imagenes/ciho.jpg", "CIHO", "CIHO"),
    ]

    vinos_encontrados = []

    # Detectar cualquier mención de vino
    for palabra_clave, imagen, caption, nombre_caracteristicas in vinos_detectar:
        if palabra_clave in texto_lower:
            if nombre_caracteristicas not in [v[2] for v in vinos_encontrados]:
                vinos_encontrados.append((imagen, caption, nombre_caracteristicas))

    # Mostrar las imágenes y gráficos encontrados
    if vinos_encontrados:
        if len(vinos_encontrados) == 1:
            # Un solo vino: lado a lado en desktop, stack en móvil
            col1, col2 = st.columns([1, 1])
            with col1:
                st.image(vinos_encontrados[0][0], caption=vinos_encontrados[0][1], width=300)
            with col2:
                grafico = crear_grafico_radar(vinos_encontrados[0][2])
                if grafico:
                    st.plotly_chart(grafico, use_container_width=True, config={'displayModeBar': False, 'responsive': True})
        else:
            # Múltiples vinos: mostrar verticalmente para mejor visualización
            st.markdown("### 📊 Perfiles de Cata")
            for imagen, caption, nombre_caract in vinos_encontrados:
                # Contenedor para cada vino
                with st.container():
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.image(imagen, caption=caption, use_column_width=True)
                    with col2:
                        grafico = crear_grafico_radar(nombre_caract)
                        if grafico:
                            st.plotly_chart(grafico, use_container_width=True, config={'displayModeBar': False, 'responsive': True})
                    st.markdown("---")  # Separador entre vinos

# Meta viewport para móviles
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
""", unsafe_allow_html=True)

# CSS personalizado para diseño profesional
st.markdown("""
<style>
    /* Importar fuente Garamond */
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600;700&display=swap');

    /* Paleta de colores profesional - Tonos vino y bodega */
    :root {
        --wine-primary: #722f37;
        --wine-secondary: #8b4049;
        --wine-light: #a85860;
        --wine-accent: #d4a574;
        --bg-cream: #faf8f3;
        --text-dark: #2c1810;
    }

    /* Aplicar Garamond globalmente */
    * {
        font-family: 'EB Garamond', 'Garamond', serif !important;
    }

    /* Fondo general */
    .stApp {
        background: linear-gradient(135deg, #faf8f3 0%, #f5f1e8 100%);
    }

    /* Header principal con efectos premium */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .main-header {
        background: linear-gradient(135deg, #722f37 0%, #8b4049 100%);
        padding: 2rem 2rem 1.5rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(114, 47, 55, 0.2);
        text-align: center;
        animation: fadeInDown 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }

    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .main-header h1 {
        color: #faf8f3;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }

    .main-header p {
        color: #d4a574;
        font-size: 1.2rem;
        font-style: italic;
        margin: 0;
        position: relative;
        z-index: 1;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #faf8f3 0%, #f0ebe0 100%);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
    }

    /* Cards de vinos en sidebar */
    .wine-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(114, 47, 55, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-left: 4px solid #722f37;
    }

    .wine-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 15px rgba(114, 47, 55, 0.2);
    }

    /* Burbujas de chat premium con animación */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .stChatMessage {
        background: white !important;
        border-radius: 15px !important;
        padding: 1.2rem !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
        animation: slideIn 0.5s ease-out;
        transition: all 0.3s ease;
    }

    .stChatMessage:hover {
        box-shadow: 0 4px 16px rgba(114, 47, 55, 0.15) !important;
        transform: translateX(5px);
    }

    /* Input del chat */
    .stChatInputContainer {
        border-top: 2px solid #d4a574;
        padding-top: 1rem;
        margin-top: 1rem;
    }

    /* Botones con efecto premium */
    .stButton > button {
        background: linear-gradient(135deg, #722f37 0%, #8b4049 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 8px rgba(114, 47, 55, 0.2);
        position: relative;
        overflow: hidden;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }

    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 6px 20px rgba(114, 47, 55, 0.4);
        background: linear-gradient(135deg, #8b4049 0%, #a85860 100%);
    }

    .stButton > button:hover::before {
        left: 100%;
    }

    .stButton > button:active {
        transform: translateY(0) scale(0.98);
    }

    /* Ajustar el textarea del input */
    [data-testid="stChatInput"] {
        padding-top: 0.5rem;
    }

    /* Headers del sidebar */
    [data-testid="stSidebar"] h2 {
        color: #722f37;
        font-weight: 700;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #d4a574;
        margin-bottom: 1.5rem;
    }

    /* Imágenes en sidebar con efecto premium */
    [data-testid="stSidebar"] img {
        border-radius: 10px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.15);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        filter: brightness(1);
        position: relative;
    }

    [data-testid="stSidebar"] img:hover {
        transform: scale(1.05) translateY(-5px);
        box-shadow: 0 8px 25px rgba(114, 47, 55, 0.3);
        filter: brightness(1.1);
    }

    /* Dividers */
    hr {
        border-color: #d4a574 !important;
        opacity: 0.3;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 1rem;
        color: #722f37;
        font-size: 0.9rem;
        border-top: 2px solid #d4a574;
        margin-top: 2rem;
    }

    /* Markdown text styling */
    .stMarkdown {
        color: #2c1810;
    }

    /* Caption styling */
    .stCaption {
        color: #8b4049 !important;
        font-weight: 500;
    }

    /* Mejorar legibilidad */
    p, li {
        line-height: 1.6;
    }

    /* Spinner personalizado */
    .stSpinner > div {
        border-top-color: #722f37 !important;
    }

    /* Input del chat sin bordes personalizados */
    [data-testid="stChatInput"] textarea {
        padding: 0.8rem 1rem !important;
        box-sizing: border-box !important;
    }

    [data-testid="stChatInput"] textarea:focus {
        outline: none !important;
    }

    [data-testid="stChatInput"] textarea:focus-visible {
        outline: none !important;
    }

    /* Contenedor personalizado del chat input */
    .chat-input-wrapper {
        padding: 0;
        margin-bottom: 0;
        overflow: visible !important;
    }

    /* Contenedor del chat input - quitar estilos que interfieren */
    [data-testid="stChatInput"] {
        background: transparent !important;
        padding: 0 1rem !important;
        overflow: visible !important;
    }

    [data-testid="stChatInput"] > div {
        background: transparent !important;
        overflow: visible !important;
    }

    /* Asegurar que el input tenga el ancho correcto con margen */
    [data-testid="stChatInput"] textarea {
        width: calc(100% - 4rem) !important;
        margin: 0 auto !important;
        display: block !important;
    }

    /* Ajustar el contenedor general del chat input */
    .stChatInputContainer {
        padding: 1rem;
        max-width: 100%;
        overflow: visible !important;
    }

    /* Forzar que TODOS los contenedores del input sean visibles */
    [data-testid="stChatInput"] * {
        overflow: visible !important;
    }

    section[data-testid="stChatInput"] {
        overflow: visible !important;
    }

    /* Espaciado del contenido principal */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* Mejoras en mensajes de chat */
    [data-testid="stChatMessageContent"] {
        padding: 0.5rem 0;
    }

    /* Efecto hover en las tarjetas del sidebar */
    [data-testid="stSidebar"] .stMarkdown {
        transition: all 0.2s ease;
    }

    /* Scrollbar personalizada */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #f5f1e8;
    }

    ::-webkit-scrollbar-thumb {
        background: #d4a574;
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #722f37;
    }

    /* Deshabilitar botones de expansión/descarga de imágenes */
    button[title="View fullscreen"],
    button[kind="icon"] {
        display: none !important;
    }

    /* Ocultar controles de imágenes */
    [data-testid="StyledFullScreenButton"] {
        display: none !important;
    }

    /* Deshabilitar interacción con imágenes */
    [data-testid="stImage"] button {
        display: none !important;
    }

    img {
        pointer-events: none !important;
    }

    /* Ocultar botón de colapsar sidebar de todas las formas posibles */
    [data-testid="collapsedControl"],
    button[kind="header"],
    button[kind="headerNoPadding"],
    .css-1dp5vir,
    .st-emotion-cache-1dp5vir {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
        position: absolute !important;
        left: -9999px !important;
    }

    /* Ocultar cualquier elemento que contenga keyboard en el texto */
    *[class*="keyboard"],
    *[aria-label*="keyboard"],
    button:has(*[class*="keyboard"]) {
        display: none !important;
        visibility: hidden !important;
    }

    /* Forzar que el sidebar esté siempre visible */
    [data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
        transform: none !important;
    }

    [data-testid="stSidebar"][aria-expanded="false"] {
        transform: none !important;
        margin-left: 0 !important;
    }

    /* Ocultar el header completo del sidebar si contiene el botón */
    section[data-testid="stSidebar"] > div > div:first-child > div:first-child {
        display: none !important;
    }

    /* ========================================
       OPTIMIZACIÓN PARA MÓVILES
       ======================================== */

    @media (max-width: 768px) {
        /* Ajustar fuentes para móvil */
        .main-header h1 {
            font-size: 1.8rem !important;
        }

        .main-header p {
            font-size: 1rem !important;
        }

        /* Reducir padding general */
        .main .block-container {
            padding: 1rem !important;
        }

        .main-header {
            padding: 1.5rem 1rem !important;
            margin-bottom: 1rem !important;
        }

        /* Optimizar burbujas de chat */
        .stChatMessage {
            padding: 0.8rem !important;
            margin-bottom: 0.8rem !important;
        }

        /* Botones más grandes para touch */
        .stButton > button {
            padding: 0.8rem 1.2rem !important;
            font-size: 1rem !important;
            min-height: 44px !important;
        }

        /* Ajustar botones de acción */
        [data-testid="column"] {
            padding: 0.5rem !important;
        }

        /* Input del chat más grande */
        [data-testid="stChatInput"] textarea {
            font-size: 16px !important;
            padding: 1rem !important;
        }

        /* Sidebar responsive */
        [data-testid="stSidebar"] {
            width: 280px !important;
        }

        [data-testid="stSidebar"] img {
            width: 100% !important;
        }

        [data-testid="stSidebar"] h2 {
            font-size: 1.3rem !important;
        }

        /* Footer más compacto */
        .footer {
            padding: 1rem 0.5rem !important;
            font-size: 0.8rem !important;
        }

        /* Gráficos más grandes y legibles en tablet */
        .js-plotly-plot {
            min-height: 450px !important;
        }

        /* Aumentar tamaño de texto en gráficos */
        .js-plotly-plot .plotly text {
            font-size: 16px !important;
        }

        .js-plotly-plot .xtick text,
        .js-plotly-plot .ytick text {
            font-size: 16px !important;
        }

        /* Reducir márgenes de imágenes */
        [data-testid="stImage"] {
            margin: 0.5rem 0 !important;
        }
    }

    @media (max-width: 480px) {
        /* Móviles muy pequeños */
        .main-header h1 {
            font-size: 1.5rem !important;
        }

        .main-header p {
            font-size: 0.9rem !important;
        }

        /* Padding mínimo */
        .main .block-container {
            padding: 0.5rem !important;
        }

        .main-header {
            padding: 1rem 0.5rem !important;
        }

        /* Botones full-width */
        .stButton > button {
            width: 100% !important;
        }

        /* Sidebar más estrecho */
        [data-testid="stSidebar"] {
            width: 260px !important;
        }

        /* Texto más pequeño en sidebar */
        [data-testid="stSidebar"] {
            font-size: 0.9rem !important;
        }

        /* Logo más pequeño */
        [data-testid="stImage"] img {
            max-width: 200px !important;
        }

        /* Gráficos optimizados para móvil pequeño */
        .js-plotly-plot {
            min-height: 400px !important;
            max-height: 550px !important;
        }

        /* Texto más grande en gráficos móvil */
        .js-plotly-plot .plotly text {
            font-size: 15px !important;
        }

        .js-plotly-plot .xtick text,
        .js-plotly-plot .ytick text,
        .js-plotly-plot .angularaxistick text {
            font-size: 16px !important;
            font-weight: 600 !important;
        }

        /* Título del gráfico más visible */
        .js-plotly-plot .gtitle {
            font-size: 20px !important;
            font-weight: bold !important;
        }
    }

    /* Optimización para landscape en móvil */
    @media (max-width: 896px) and (orientation: landscape) {
        .main-header {
            padding: 1rem !important;
            margin-bottom: 0.5rem !important;
        }

        .main-header h1 {
            font-size: 1.5rem !important;
        }

        .stChatMessage {
            padding: 0.6rem !important;
            margin-bottom: 0.5rem !important;
        }
    }

    /* Evitar zoom en inputs en iOS */
    @supports (-webkit-touch-callout: none) {
        input, textarea, select {
            font-size: 16px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header principal con logo centrado
st.markdown("""
<div style="text-align: center; margin-bottom: 1rem;">
""", unsafe_allow_html=True)

# Logo centrado
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.image("imagenes/logo.png", use_container_width=True)

st.markdown("""
</div>
<div class="main-header" style="padding-top: 1rem;">
    <h1 style="margin-top: 0;">Calar Viejo</h1>
    <p>Bodega Marín Perona</p>
    <p style="font-size: 1rem; margin-top: 0.5rem;">Vino sin prisas. Aquí manda la viña, no la fábrica.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar con información
with st.sidebar:
    st.header("🍇 Nuestra Gama")

    st.markdown('<div style="margin-bottom: 1.5rem;"></div>', unsafe_allow_html=True)

    # CIHO
    st.image("imagenes/ciho.jpg", width="stretch")
    st.markdown("**🍯 CIHO** (dulce)")
    st.caption("Tu primera copa sin miedo. Dulce y refrescante.")
    st.markdown('<hr style="margin: 1.5rem 0;">', unsafe_allow_html=True)

    # Blanco Airén
    st.image("imagenes/airen.jpg", width="stretch")
    st.markdown("**🌾 Blanco Airén**")
    st.caption("Fresco, fácil. De terraza y tardes largas.")
    st.markdown('<hr style="margin: 1.5rem 0;">', unsafe_allow_html=True)

    # Tinto Joven Tempranillo
    st.image("imagenes/tempranillo.jpg", width="stretch")
    st.markdown("**🍷 Tinto Joven Tempranillo**")
    st.caption("Frutal, directo. Perfecto para tapas.")
    st.markdown('<hr style="margin: 1.5rem 0;">', unsafe_allow_html=True)

    # Crianza
    st.image("imagenes/crianza.jpg", width="stretch")
    st.markdown("**🍇 Crianza** (6 meses)")
    st.caption("Equilibrado, madera suave. Elegancia accesible.")
    st.markdown('<hr style="margin: 1.5rem 0;">', unsafe_allow_html=True)

    # Reserva
    st.image("imagenes/reserva.jpg", width="stretch")
    st.markdown("**👑 Reserva** (12 meses)")
    st.caption("Serio pero cercano. Para ocasiones especiales.")

    st.markdown("---")
    st.markdown('<p style="text-align: center; font-weight: 600; color: #722f37; font-size: 1.1rem; margin-top: 2rem;">Vino sin prisas.</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #8b4049; font-style: italic;">Aquí manda la viña, no la fábrica.</p>', unsafe_allow_html=True)

    st.divider()

    if st.button("🔄 Nueva Conversación"):
        st.session_state.messages = []
        mensaje_bienvenida = {
            "role": "assistant",
            "content": "¡Hola! Soy Alberto, de Bodega Marín Perona 🍇 Aquí llevamos generaciones haciendo vino con calma, sin prisas. Cuéntame, ¿qué estás buscando? ¿Terraza con amigos, cena tranquila o algo especial? Te ayudo a encontrar tu vino perfecto."
        }
        st.session_state.messages.append(mensaje_bienvenida)
        st.rerun()

    st.markdown("---")

    # ===== SISTEMA DE FEEDBACK CON TEXTO EN SIDEBAR =====
    st.markdown("### 💬 Feedback")

    # Contar mensajes del usuario (sin contar el de bienvenida)
    mensajes_usuario = [msg for msg in st.session_state.messages if msg["role"] == "user"]

    # Mostrar feedback si hay al menos 1 mensaje del usuario
    if len(mensajes_usuario) >= 1:
        # Buscar el último mensaje del asistente (excluyendo bienvenida)
        ultimo_asistente = None
        for msg in reversed(st.session_state.messages):
            if msg["role"] == "assistant":
                # Verificar que no es el mensaje de bienvenida
                if not msg["content"].startswith("¡Ey! Bienvenido"):
                    ultimo_asistente = msg
                    break

        if ultimo_asistente:
            st.caption("¿Qué te pareció la última recomendación?")

            # Selector de tipo de feedback
            tipo_feedback = st.radio(
                "Tipo:",
                ["👍 Útil", "👎 Mejorar"],
                horizontal=True,
                label_visibility="collapsed"
            )

            # Campo de texto para feedback detallado
            comentario_feedback = st.text_area(
                "Tu opinión (opcional):",
                placeholder="Cuéntanos qué te gustó o qué podríamos mejorar...",
                max_chars=500,
                height=100
            )

            # Botón de envío
            if st.button("📤 Enviar Feedback", type="primary", use_container_width=True):
                # Buscar la pregunta del usuario
                pregunta = ""
                for i in range(len(st.session_state.messages) - 1, -1, -1):
                    if st.session_state.messages[i]["role"] == "user":
                        pregunta = st.session_state.messages[i]["content"]
                        break

                # Determinar tipo (positivo/negativo)
                tipo = "positivo" if "👍" in tipo_feedback else "negativo"

                # Detectar vino mencionado
                vino = detectar_vino_en_respuesta(ultimo_asistente["content"])

                # Guardar feedback
                guardar_feedback(
                    pregunta,
                    ultimo_asistente["content"],
                    vino,
                    tipo,
                    comentario_feedback
                )

                if tipo == "positivo":
                    st.balloons()
                    st.success("¡Gracias por tu feedback! 🍷")
                else:
                    st.info("Gracias, nos ayuda a mejorar")
    else:
        st.info("Chatea para dar feedback")

    st.markdown("---")

    # Panel de Análisis de Feedback
    with st.expander("📊 Análisis de Feedback", expanded=False):
        df_feedback = obtener_estadisticas_feedback()

        if not df_feedback.empty:
            st.markdown("**Resumen General**")

            total = len(df_feedback)
            positivos = len(df_feedback[df_feedback['feedback_tipo'] == 'positivo'])
            negativos = len(df_feedback[df_feedback['feedback_tipo'] == 'negativo'])

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total", total)
                st.metric("👍 Positivos", positivos)
            with col2:
                tasa_satisfaccion = (positivos / total * 100) if total > 0 else 0
                st.metric("Satisfacción", f"{tasa_satisfaccion:.0f}%")
                st.metric("👎 Negativos", negativos)

            st.markdown("**Por Vino**")

            vinos_stats = df_feedback.groupby('vino_recomendado').agg({
                'feedback_tipo': lambda x: (x == 'positivo').sum(),
                'id': 'count'
            }).reset_index()
            vinos_stats.columns = ['Vino', 'Positivos', 'Total']
            vinos_stats['Satisfacción'] = (vinos_stats['Positivos'] / vinos_stats['Total'] * 100).round(0)

            for _, row in vinos_stats.iterrows():
                st.markdown(f"**{row['Vino']}**: {row['Satisfacción']:.0f}% ({row['Total']} recomendaciones)")

            if st.button("📥 Exportar Datos", key="btn_exportar_feedback"):
                csv = df_feedback.to_csv(index=False)
                st.download_button(
                    label="Descargar CSV",
                    data=csv,
                    file_name=f"feedback_chatbot_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    key="btn_download_csv"
                )
        else:
            st.info("Aún no hay feedback registrado. Los usuarios pueden dar feedback con 👍/👎")

    st.markdown("---")
    st.markdown('<p style="text-align: center; color: #722f37; font-weight: 600; margin-bottom: 0.3rem;">Bodega Marín Perona</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #8b4049; font-size: 0.85rem; margin-bottom: 0.5rem;">Calar Viejo • Tradición Familiar</p>', unsafe_allow_html=True)
    st.caption("Powered by Groq AI")

# ===== BOTONES DE ACCIÓN RÁPIDA =====
st.markdown('<div style="margin: 1.5rem 0;">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ⚡ Acciones Rápidas")

    # Botón de preguntas comunes
    if st.button("💬 Preguntas Comunes", use_container_width=True, key="btn_preguntas"):
        prompt = "Muéstrame las preguntas más comunes sobre vuestros vinos"
        # Agregar mensaje del usuario al historial
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generar respuesta del asistente
        with st.spinner("Pensando en tu copa perfecta..."):
            respuesta = obtener_respuesta_groq(st.session_state.messages)

        # Agregar respuesta al historial
        st.session_state.messages.append({"role": "assistant", "content": respuesta})
        st.rerun()

    # Botón de consejero de regalo
    if st.button("🎁 Consejero de Regalo", use_container_width=True, key="btn_regalo"):
        prompt = "Necesito ayuda para elegir un vino como regalo"
        # Agregar mensaje del usuario al historial
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generar respuesta del asistente
        with st.spinner("Pensando en tu copa perfecta..."):
            respuesta = obtener_respuesta_groq(st.session_state.messages)

        # Agregar respuesta al historial
        st.session_state.messages.append({"role": "assistant", "content": respuesta})
        st.rerun()

with col2:
    st.markdown("### 🔗 Enlaces Útiles")

    # Botón de comprar (enlace a web Marín Perona)
    st.link_button(
        "🛒 Comprar Vinos",
        "https://marinperona.es/contacto-pedidos/",
        use_container_width=True
    )

    # Botón de contacto WhatsApp
    st.link_button(
        "📱 Contactar por WhatsApp",
        "https://wa.me/34633343323",
        use_container_width=True
    )

st.markdown('</div>', unsafe_allow_html=True)
st.divider()

# Mostrar historial de chat
for idx, mensaje in enumerate(st.session_state.messages):
    avatar = "🍷" if mensaje["role"] == "assistant" else "user"
    with st.chat_message(mensaje["role"], avatar=avatar):
        st.markdown(mensaje["content"])
        # Si es un mensaje del asistente, mostrar imagen del vino si aplica
        if mensaje["role"] == "assistant":
            mostrar_imagen_vino(mensaje["content"])

# Input del usuario con contenedor personalizado
st.markdown('<div class="chat-input-wrapper">', unsafe_allow_html=True)
if prompt := st.chat_input("Cuéntame el plan o qué buscas..."):
    # Agregar mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)

    # Obtener y mostrar respuesta del asistente
    with st.chat_message("assistant", avatar="🍷"):
        with st.spinner("Pensando en tu copa perfecta..."):
            respuesta = obtener_respuesta_groq(st.session_state.messages)
            st.markdown(respuesta)
            # Mostrar imagen del vino si se recomienda alguno
            mostrar_imagen_vino(respuesta)

    # Agregar respuesta al historial
    st.session_state.messages.append({"role": "assistant", "content": respuesta})

st.markdown('</div>', unsafe_allow_html=True)

# Footer profesional
st.markdown("""
<div class="footer">
    <p style="font-size: 1.1rem; font-weight: 600; color: #722f37; margin-bottom: 0.5rem;">
        🍇 No te compliques: si te gusta, es el bueno.
    </p>
    <p style="font-style: italic; color: #8b4049; margin-bottom: 1rem;">
        A tu ritmo, como el vino.
    </p>
    <p style="font-size: 0.85rem; color: #a85860;">
        Bodega Marín Perona • Calar Viejo • Tradición Familiar
    </p>
</div>
""", unsafe_allow_html=True)

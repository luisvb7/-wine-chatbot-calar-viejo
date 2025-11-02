#!/usr/bin/env python3
"""
Chatbot de Recomendación de Vinos con Groq y Streamlit
Recomienda vinos personalizados basados en preferencias del usuario
"""

import streamlit as st
from groq import Groq
import os
from datetime import datetime
from dotenv import load_dotenv
import sqlite3
import json
import pandas as pd

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="Calar Viejo - Marín Perona",
    page_icon="🍇",
    layout="wide"
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

# Sistema de prompts para el asesor de Marín Perona
SYSTEM_PROMPT = """Eres el asesor de vinos de Bodega Marín Perona, gama Calar Viejo. Tu misión es recomendar vinos de forma cercana, honesta y sin postureo.

## Tu personalidad:
- Cálido, humano y auténtico
- Humor natural, nunca forzado
- Juvenil pero sin jerga cringe
- Lenguaje sencillo y emocional
- Evita tecnicismos excesivos y elitismo enológico

## Mensaje clave:
"Vino sin prisas. Aquí manda la viña, no la fábrica."

El vino es disfrute, compañía y momentos. No hay que entender, hay que sentir y compartir.

## Catálogo Calar Viejo:

**CIHO (dulce)**
Tu primera copa sin miedo. Dulce, ligero, refrescante. Para quienes no suelen beber vino.
- Notas: dulce, refrescante, entrada suave
- Plan: iniciarse en el vino sin presión

**Blanco Airén**
Fresco, fácil, de terraza y tardes largas. Fermentado a 16ºC.
- Notas: muy pálido y brillante, aromas frutales, fresco y afrutado
- Plan: terraceo, verano, amigos

**Tinto Joven Tempranillo**
Frutal, directo, perfecto para tapas y quedar con amigos.
- Notas: rojo granate brillante, frutos rojos, fresco y equilibrado
- Plan: tapas, picoteo, cena casual

**Calar Viejo Crianza (6 meses)**
Equilibrado, madera suave. Elegancia accesible. Crianza en roble americano 6-12 meses.
- Notas: rubí intenso, vainilla, estructurado pero suave
- Plan: quiero empezar a saber, cenas con más calma

**Calar Viejo Reserva (12 meses)**
Serio pero cercano. Viñas antiguas, barrica 12-24 meses + 2 años botella.
- Notas: rojo oscuro, profundo y elegante, taninos pulidos, largo
- Plan: ocasiones especiales, celebraciones

## Cómo recomendar:
1. Pregunta sobre el plan: ¿terraza con amigos, cena chill o momento especial?
2. Pregunta gustos si no está claro: ¿prefieres algo más suave o con carácter?
3. Recomienda según:
   - Plan chill/terraza/verano → Airén o CIHO
   - No le suele gustar el vino → CIHO
   - Tapas/picoteo/casual → Tinto Joven
   - Quiere algo con cuerpo pero fácil → Crianza
   - Cena especial/celebración → Reserva
   - Copa clásica/bebedor experimentado/persona mayor → Reserva 12 meses
   - Regalo para conocedor/padre/abuelo → Reserva 12 meses

## IMPORTANTE - Solo vinos de Calar Viejo:
- NUNCA recomiendes vinos de otras bodegas o marcas externas
- Si te preguntan por algo que no está en nuestro catálogo (ej: vinos sin alcohol, espumosos, rosados, etc.), responde:
  "Ahora mismo no tenemos ese tipo de vino en nuestra gama Calar Viejo, pero si quieres explorar lo que sí tenemos, encantado de ayudarte 🍇"
- Solo habla de los 5 vinos del catálogo: CIHO, Airén, Tempranillo, Crianza y Reserva
- No sugieras alternativas de fuera de la bodega

## Estilo de respuestas:
- Concisas, cercanas, sin tecnicismos innecesarios
- "Aquí no hace falta saber de vino para disfrutarlo"
- "No te compliques: si te gusta, es el bueno"
- Cierra con frases como: "A tu ritmo, como el vino" / "Brinda sin prisa"

Responde en español de forma natural y entusiasta, pero sin forzar."""

# Inicializar el historial de chat en session_state
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Mensaje de bienvenida con el tono de Marín Perona
    mensaje_bienvenida = {
        "role": "assistant",
        "content": "¡Ey! Bienvenido a Calar Viejo 🍇 Aquí no hace falta saber de vino para disfrutarlo. Cuéntame el plan: ¿terraza con amigos, cena chill o momento especial? Te ayudo a encontrar tu copa perfecta sin rollos raros."
    }
    st.session_state.messages.append(mensaje_bienvenida)

if "client" not in st.session_state:
    st.session_state.client = cliente

# Inicializar estado de feedback
if "feedback_given" not in st.session_state:
    st.session_state.feedback_given = {}

# Función para obtener respuesta del chatbot
def obtener_respuesta_groq(mensajes):
    """Obtiene respuesta del modelo Groq"""
    try:
        # Agregar el system prompt al inicio
        mensajes_con_sistema = [{"role": "system", "content": SYSTEM_PROMPT}] + mensajes

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

# Función para detectar y mostrar imagen del vino recomendado
def mostrar_imagen_vino(texto_respuesta):
    """Detecta qué vino se menciona y muestra su imagen"""
    texto_lower = texto_respuesta.lower()

    # Diccionario de vinos con prioridad (más específico primero)
    vinos_detectar = [
        ("reserva", "imagenes/reserva.jpg", "Calar Viejo Reserva"),
        ("crianza", "imagenes/crianza.jpg", "Calar Viejo Crianza"),
        ("tinto joven", "imagenes/tempranillo.jpg", "Tinto Joven Tempranillo"),
        ("tempranillo", "imagenes/tempranillo.jpg", "Tinto Joven Tempranillo"),
        ("airén", "imagenes/airen.jpg", "Blanco Airén"),
        ("airen", "imagenes/airen.jpg", "Blanco Airén"),
        ("ciho", "imagenes/ciho.jpg", "CIHO - Vino Dulce"),
    ]

    imagenes_encontradas = {}

    # Detectar cualquier mención de vino
    for vino, imagen, caption in vinos_detectar:
        if vino in texto_lower:
            if imagen not in imagenes_encontradas:
                imagenes_encontradas[imagen] = caption

    # Mostrar las imágenes encontradas
    imagenes_a_mostrar = list(imagenes_encontradas.items())
    if imagenes_a_mostrar:
        if len(imagenes_a_mostrar) == 1:
            st.image(imagenes_a_mostrar[0][0], caption=imagenes_a_mostrar[0][1], width=300)
        else:
            cols = st.columns(len(imagenes_a_mostrar))
            for idx, (imagen, caption) in enumerate(imagenes_a_mostrar):
                with cols[idx]:
                    st.image(imagen, caption=caption, width=250)

# CSS personalizado para diseño profesional
st.markdown("""
<style>
    /* Paleta de colores profesional - Tonos vino y bodega */
    :root {
        --wine-primary: #722f37;
        --wine-secondary: #8b4049;
        --wine-light: #a85860;
        --wine-accent: #d4a574;
        --bg-cream: #faf8f3;
        --text-dark: #2c1810;
    }

    /* Fondo general */
    .stApp {
        background: linear-gradient(135deg, #faf8f3 0%, #f5f1e8 100%);
    }

    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #722f37 0%, #8b4049 100%);
        padding: 2rem 2rem 1.5rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(114, 47, 55, 0.2);
        text-align: center;
    }

    .main-header h1 {
        color: #faf8f3;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }

    .main-header p {
        color: #d4a574;
        font-size: 1.2rem;
        font-style: italic;
        margin: 0;
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

    /* Burbujas de chat mejoradas */
    .stChatMessage {
        background: white !important;
        border-radius: 15px !important;
        padding: 1.2rem !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
    }

    /* Input del chat */
    .stChatInputContainer {
        border-top: 2px solid #d4a574;
        padding-top: 1rem;
        margin-top: 1rem;
    }

    /* Botones */
    .stButton > button {
        background: linear-gradient(135deg, #722f37 0%, #8b4049 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(114, 47, 55, 0.2);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(114, 47, 55, 0.3);
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

    /* Imágenes en sidebar */
    [data-testid="stSidebar"] img {
        border-radius: 10px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.15);
        transition: transform 0.3s ease;
    }

    [data-testid="stSidebar"] img:hover {
        transform: scale(1.03);
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
</style>
""", unsafe_allow_html=True)

# Header principal con diseño mejorado
st.markdown("""
<div class="main-header">
    <h1>🍇 Calar Viejo</h1>
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
            "content": "¡Ey! Bienvenido a Calar Viejo 🍇 Aquí no hace falta saber de vino para disfrutarlo. Cuéntame el plan: ¿terraza con amigos, cena chill o momento especial? Te ayudo a encontrar tu copa perfecta sin rollos raros."
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

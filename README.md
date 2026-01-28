# 🍷 Chatbot Calar Viejo - Bodega Marín Perona

Chatbot inteligente para recomendación de vinos de la gama Calar Viejo, con sistema RAG (Retrieval Augmented Generation) y visualizaciones interactivas.

## 🚀 Características

- **Sistema RAG con ChromaDB**: Recomendaciones inteligentes basadas en base de datos vectorial
- **Gráficos de radar interactivos**: Visualización de notas de cata con Plotly
- **Personalidad de Alberto**: Dueño de la bodega, representa la tradición familiar
- **Adaptación automática**: El lenguaje se adapta según el usuario
- **UX Premium**: Efectos y animaciones elegantes
- **Memoria por sesión**: Cada usuario tiene su historial aislado

## 📦 Instalación Local

```bash
# Clonar el repositorio
git clone https://github.com/luisvb7/-wine-chatbot-calar-viejo.git
cd -wine-chatbot-calar-viejo

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env con tu API key de Groq
echo "GROQ_API_KEY=tu-api-key-aqui" > .env

# Inicializar la base de datos vectorial
python3 inicializar_rag.py

# Ejecutar la aplicación
streamlit run wine_chatbot_app.py
```

## 🌐 Deploy en Streamlit Cloud

### Paso 1: Preparar el repositorio
Tu repositorio ya está listo en GitHub con todos los archivos necesarios.

### Paso 2: Ir a Streamlit Cloud
1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Inicia sesión con tu cuenta de GitHub

### Paso 3: Crear nueva app
1. Haz clic en "New app"
2. Selecciona tu repositorio: `luisvb7/-wine-chatbot-calar-viejo`
3. Branch: `main`
4. Main file path: `wine_chatbot_app.py`

### Paso 4: Configurar Secrets
En "Advanced settings" > "Secrets", añade:

```toml
GROQ_API_KEY = "tu-groq-api-key-aqui"
```

**Nota**: Necesitas obtener una API key gratuita de Groq en [console.groq.com](https://console.groq.com)

### Paso 5: Deploy
Haz clic en "Deploy" y espera unos minutos. ¡Tu chatbot estará en vivo!

## 📊 Catálogo de Vinos

- **CIHO (Dulce)** - 4€
- **Blanco Airén** - 3.5€
- **Tinto Joven Tempranillo** - 4€
- **Calar Viejo Crianza (6 meses)** - 5.5€
- **Calar Viejo Reserva (12 meses)** - 9€

## 🔗 Enlaces

- **Comprar**: https://marinperona.es/contacto-pedidos/
- **WhatsApp**: 633 343 323

## 🛠️ Tecnologías

- Streamlit
- Groq (LLM)
- ChromaDB (Base de datos vectorial)
- Plotly (Visualizaciones)
- Sentence Transformers (Embeddings)

## 🌐 Widget para Integración Web

¿Quieres añadir el chatbot a tu web? En la carpeta **`widget/`** encontrarás:

- **`widget-chatbot.js`** → Botón flotante para tu web
- **`ejemplo-widget.html`** → Página de demostración
- **`INSTRUCCIONES-WIDGET.md`** → Guía completa de instalación

El widget crea un botón flotante 🍷 en tu web que abre el chatbot en un iframe elegante.

**[Ver instrucciones de instalación →](widget/INSTRUCCIONES-WIDGET.md)**

## 📝 Estructura del Proyecto

```
├── wine_chatbot_app.py          # 🚀 Aplicación principal del chatbot
├── vinos_data.py                # Base de conocimiento de vinos
├── vinos_caracteristicas.py     # Características para gráficos
├── inicializar_rag.py           # Script para inicializar ChromaDB
├── test_rag.py                  # Tests del sistema RAG
├── requirements.txt             # Dependencias
├── chroma_db/                   # Base de datos vectorial
├── imagenes/                    # Imágenes de vinos y logo
├── widget/                      # 🌐 Archivos para integrar en web
│   ├── widget-chatbot.js        #    → Widget flotante
│   ├── ejemplo-widget.html      #    → Demo del widget
│   ├── INSTRUCCIONES-WIDGET.md  #    → Guía de instalación
│   └── README.md                #    → Info de la carpeta
└── .streamlit/
    └── config.toml              # Configuración de Streamlit
```

**⚠️ Importante:**
- Los archivos en `widget/` son **solo para instalar en tu web**
- **NO afectan** al funcionamiento del chatbot en Streamlit Cloud
- Streamlit Cloud solo ejecuta `wine_chatbot_app.py`

## 👨‍💼 Autor

Luis Villar Balmy - Bodega Marín Perona
*"Vino sin prisas. Aquí manda la viña, no la fábrica."*

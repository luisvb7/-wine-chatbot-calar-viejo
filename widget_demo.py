"""
Demo del Widget de Integración Web
Bodega Marín Perona - Chatbot Calar Viejo
"""

import streamlit as st
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(
    page_title="Widget Demo - Chatbot Calar Viejo",
    page_icon="🍷",
    layout="wide"
)

# Leer el contenido del HTML de ejemplo
with open('widget/ejemplo-widget.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Leer el JavaScript del widget
with open('widget/widget-chatbot.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Actualizar la URL en el JavaScript para apuntar a la app principal
js_content = js_content.replace(
    "chatbotUrl: 'http://localhost:8501/?embed=true'",
    "chatbotUrl: 'https://wine-chatbot-calar-viejo.streamlit.app/?embed=true'"
)

# Insertar el JavaScript en el HTML
html_with_js = html_content.replace(
    '<script src="widget-chatbot.js"></script>',
    f'<script>{js_content}</script>'
)

# Mostrar el HTML con el widget
components.html(html_with_js, height=800, scrolling=True)

# Información adicional
st.markdown("---")
st.markdown("""
### 📋 Sobre este demo

Este es un ejemplo de cómo se vería el widget del chatbot integrado en tu página web.

**Características:**
- ✅ Botón flotante en la esquina inferior derecha
- ✅ Diseño responsive (se adapta a móvil)
- ✅ Colores personalizados de Calar Viejo
- ✅ Integración lista para WordPress

**Para instalar en tu web:**
1. Descarga el archivo `widget-chatbot.js` del repositorio
2. Súbelo a tu servidor en `/js/`
3. Añade `<script src="/js/widget-chatbot.js"></script>` antes de `</body>`

Ver instrucciones completas en el repositorio: [GitHub](https://github.com/luisvb7/-wine-chatbot-calar-viejo)
""")

# 🍷 Widget Chatbot Calar Viejo - Instrucciones de Instalación

## 📋 Descripción

Widget flotante que integra el chatbot de Alberto (asesor de vinos) en la web de Marín Perona. Aparece como un botón flotante en la esquina inferior derecha y se expande en un chat completo.

---

## 🚀 Instalación Rápida (3 pasos)

### **Paso 1: Subir el archivo JavaScript**

1. Descarga el archivo `widget-chatbot.js`
2. Súbelo a tu servidor web en la carpeta `/js/` o `/assets/js/`
3. Anota la ruta completa (ejemplo: `/js/widget-chatbot.js`)

### **Paso 2: Configurar la URL del chatbot**

Abre `widget-chatbot.js` y en la línea 14, cambia la URL:

```javascript
chatbotUrl: 'https://wine-chatbot-calar-viejo.streamlit.app',
```

Por la URL real de tu chatbot en Streamlit Cloud.

### **Paso 3: Añadir a tu web**

Añade esta línea **antes de cerrar el `</body>`** en todas las páginas donde quieras el widget:

```html
<script src="/js/widget-chatbot.js"></script>
```

**¡Listo!** El widget aparecerá automáticamente.

---

## 🎨 Personalización

### **Cambiar posición del botón**

En `widget-chatbot.js`, línea 17:

```javascript
position: 'bottom-right',  // Opciones: bottom-right, bottom-left, top-right, top-left
```

### **Cambiar colores**

Líneas 20-21:

```javascript
primaryColor: '#722f37',    // Color principal (granate)
secondaryColor: '#8b4049',  // Color secundario
```

### **Cambiar tamaños**

Líneas 24-26:

```javascript
buttonSize: '60px',      // Tamaño del botón flotante
chatWidth: '400px',      // Ancho del chat en desktop
chatHeight: '600px',     // Alto del chat
```

### **Cambiar texto**

Líneas 29-30:

```javascript
buttonIcon: '🍷',                        // Emoji del botón
buttonTooltip: 'Asesor de Vinos Alberto', // Texto al pasar el mouse
```

---

## 📱 Comportamiento en Móvil

En móviles (pantallas < 768px):
- El chat ocupa **pantalla completa** automáticamente
- Mejor experiencia de usuario
- Se puede desactivar editando la línea 35:

```javascript
mobileFullscreen: true,  // Cambiar a false para mantener tamaño fijo
```

---

## 🔧 Instalación en diferentes plataformas

### **WordPress**

1. Ir a **Apariencia → Editor de temas**
2. Editar `footer.php`
3. Antes de `</body>`, añadir:

```html
<script src="<?php echo get_template_directory_uri(); ?>/js/widget-chatbot.js"></script>
```

4. Subir `widget-chatbot.js` a `/wp-content/themes/tu-tema/js/`

### **HTML estático**

Añadir en todas las páginas `.html`:

```html
<script src="/js/widget-chatbot.js"></script>
```

### **React / Next.js**

En tu componente Layout o `_app.js`:

```javascript
useEffect(() => {
  const script = document.createElement('script');
  script.src = '/js/widget-chatbot.js';
  script.async = true;
  document.body.appendChild(script);
}, []);
```

### **PHP**

En tu `footer.php` o plantilla:

```php
<script src="/js/widget-chatbot.js"></script>
```

---

## ✅ Verificación

Después de instalar:

1. Abre tu web en un navegador
2. Deberías ver el botón 🍷 en la esquina inferior derecha
3. Al hacer clic, se abre el chat
4. Al pasar el mouse sobre el botón, aparece "Asesor de Vinos Alberto"

---

## 🐛 Solución de Problemas

### **El widget no aparece**

1. Verifica que la ruta del script sea correcta
2. Abre la consola del navegador (F12) y busca errores
3. Verifica que el archivo `widget-chatbot.js` esté accesible

### **El chat no carga**

1. Verifica que la URL del chatbot en línea 14 sea correcta
2. Asegúrate de que tu chatbot esté desplegado en Streamlit Cloud
3. Verifica que no haya bloqueadores de contenido (adblockers)

### **El botón no se ve bien**

1. Puede haber conflictos CSS con tu tema
2. Añade `!important` a los estilos problemáticos en el archivo JS
3. Aumenta el `z-index` si está detrás de otros elementos

---

## 🎯 Funcionalidades Incluidas

✅ **Botón flotante animado** con efecto pulse
✅ **Tooltip informativo** al pasar el mouse
✅ **Apertura/cierre suave** con animaciones
✅ **Botón de cerrar (×)** dentro del chat
✅ **Tecla Escape** para cerrar
✅ **Responsive** automático en móvil
✅ **Vibración háptica** en dispositivos compatibles
✅ **Sin dependencias** (JavaScript puro)

---

## 📊 Análisis y Seguimiento

Para ver estadísticas de uso, puedes añadir:

```javascript
// Después de la línea 173 en widget-chatbot.js
if (isOpen) {
    // Google Analytics
    gtag('event', 'chat_opened', {
        'event_category': 'engagement',
        'event_label': 'chatbot'
    });
}
```

---

## 🔐 Seguridad

El widget:
- ✅ No recoge datos del usuario
- ✅ No usa cookies
- ✅ Carga el chatbot en iframe seguro
- ✅ Cumple con RGPD

---

## 📞 Soporte

Si tienes problemas con la instalación:

1. Revisa este documento completo
2. Verifica la consola del navegador (F12)
3. Asegúrate de que todos los archivos estén en las rutas correctas

---

## 🎨 Ejemplo Visual

```
┌─────────────────────────────────┐
│                                 │
│     Tu Página Web               │
│     marinperona.es              │
│                                 │
│                                 │
│                          ┌────┐ │
│                          │ 🍷 │ │ ← Botón flotante
│                          └────┘ │
└─────────────────────────────────┘

Al hacer clic:

┌─────────────────────────────────┐
│                        ┌──────┐ │
│     Tu Página Web      │  ×   │ │
│     marinperona.es     ├──────┤ │
│                        │      │ │
│                        │ Chat │ │
│                        │      │ │
│                        │Alberto│ │
│                        │      │ │
│                        └──────┘ │
└─────────────────────────────────┘
```

---

## 📝 Archivos Incluidos

1. **`widget-chatbot.js`** - Widget completo (listo para usar)
2. **`ejemplo-widget.html`** - Página de demostración
3. **`INSTRUCCIONES-WIDGET.md`** - Este documento

---

## 🚀 Siguiente Paso

Para publicar tu chatbot en Streamlit Cloud (si aún no lo has hecho):

1. Ve a https://share.streamlit.io
2. Conecta tu repositorio GitHub
3. Selecciona `wine_chatbot_app.py`
4. Añade tu `GROQ_API_KEY` en Secrets
5. Copia la URL generada y ponla en el archivo `widget-chatbot.js` (línea 14)

---

**¡Disfruta de tu nuevo asistente virtual! 🍷**

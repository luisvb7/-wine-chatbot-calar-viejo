/**
 * Widget Flotante - Chatbot Calar Viejo
 * Bodega Marín Perona
 *
 * Instrucciones de instalación:
 * 1. Sube este archivo a tu servidor web
 * 2. Añade en el HTML: <script src="/js/widget-chatbot.js"></script>
 * 3. El widget aparecerá automáticamente en todas las páginas
 */

(function() {
    'use strict';

    // Configuración
    const CONFIG = {
        // URL de tu chatbot en Streamlit Cloud
        chatbotUrl: 'https://wine-chatbot-calar-viejo.streamlit.app/?embed=true',

        // Posición del botón (bottom-right, bottom-left, top-right, top-left)
        position: 'bottom-right',

        // Colores personalizados (colores de Calar Viejo)
        primaryColor: '#722f37',
        secondaryColor: '#8b4049',

        // Tamaños
        buttonSize: '60px',
        chatWidth: '400px',
        chatHeight: '600px',

        // Textos
        buttonIcon: '🍷',
        buttonTooltip: 'Asesor de Vinos Alberto',

        // Mobile
        mobileFullscreen: true
    };

    // Estilos CSS
    const styles = `
        .wine-chatbot-button {
            position: fixed;
            ${CONFIG.position.includes('bottom') ? 'bottom: 20px;' : 'top: 20px;'}
            ${CONFIG.position.includes('right') ? 'right: 20px;' : 'left: 20px;'}
            width: ${CONFIG.buttonSize};
            height: ${CONFIG.buttonSize};
            border-radius: 50%;
            background: linear-gradient(135deg, ${CONFIG.primaryColor}, ${CONFIG.secondaryColor});
            color: white;
            font-size: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(114, 47, 55, 0.4);
            z-index: 999999;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: none;
            user-select: none;
            -webkit-tap-highlight-color: transparent;
        }

        .wine-chatbot-button:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 6px 30px rgba(114, 47, 55, 0.5);
        }

        .wine-chatbot-button:active {
            transform: translateY(0) scale(0.95);
        }

        .wine-chatbot-button::after {
            content: '${CONFIG.buttonTooltip}';
            position: absolute;
            ${CONFIG.position.includes('right') ? 'right: 70px;' : 'left: 70px;'}
            background: rgba(44, 24, 16, 0.95);
            color: white;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 14px;
            font-family: 'EB Garamond', serif;
            white-space: nowrap;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s;
        }

        .wine-chatbot-button:hover::after {
            opacity: 1;
        }

        .wine-chatbot-pulse {
            animation: wine-pulse 2s infinite;
        }

        @keyframes wine-pulse {
            0%, 100% {
                box-shadow: 0 4px 20px rgba(114, 47, 55, 0.4);
            }
            50% {
                box-shadow: 0 4px 30px rgba(114, 47, 55, 0.7);
            }
        }

        .wine-chatbot-container {
            position: fixed;
            ${CONFIG.position.includes('bottom') ? 'bottom: 90px;' : 'top: 90px;'}
            ${CONFIG.position.includes('right') ? 'right: 20px;' : 'left: 20px;'}
            width: ${CONFIG.chatWidth};
            height: ${CONFIG.chatHeight};
            border: none;
            border-radius: 15px;
            box-shadow: 0 10px 50px rgba(0, 0, 0, 0.2);
            z-index: 999998;
            display: none;
            background: white;
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .wine-chatbot-container.open {
            display: block;
            animation: slideIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(20px) scale(0.95);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }

        .wine-chatbot-iframe {
            width: 100%;
            height: 100%;
            border: none;
        }

        .wine-chatbot-close {
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(114, 47, 55, 0.9);
            color: white;
            border: none;
            border-radius: 50%;
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            z-index: 1000000;
            font-size: 20px;
            line-height: 1;
            transition: all 0.3s;
        }

        .wine-chatbot-close:hover {
            background: rgba(139, 64, 73, 1);
            transform: rotate(90deg);
        }

        /* Mobile Styles */
        @media (max-width: 768px) {
            .wine-chatbot-container {
                width: 100vw !important;
                height: 100vh !important;
                bottom: 0 !important;
                right: 0 !important;
                left: 0 !important;
                top: 0 !important;
                border-radius: 0 !important;
            }

            .wine-chatbot-button {
                bottom: 15px;
                right: 15px;
            }
        }
    `;

    // Inyectar estilos
    const styleSheet = document.createElement('style');
    styleSheet.textContent = styles;
    document.head.appendChild(styleSheet);

    // Crear botón flotante
    const button = document.createElement('div');
    button.className = 'wine-chatbot-button wine-chatbot-pulse';
    button.innerHTML = CONFIG.buttonIcon;
    button.setAttribute('aria-label', 'Abrir asesor de vinos');
    button.setAttribute('role', 'button');

    // Crear contenedor del chat
    const container = document.createElement('div');
    container.className = 'wine-chatbot-container';

    // Crear botón de cerrar
    const closeBtn = document.createElement('button');
    closeBtn.className = 'wine-chatbot-close';
    closeBtn.innerHTML = '×';
    closeBtn.setAttribute('aria-label', 'Cerrar chat');

    // Crear iframe
    const iframe = document.createElement('iframe');
    iframe.className = 'wine-chatbot-iframe';
    iframe.src = CONFIG.chatbotUrl;
    iframe.setAttribute('allow', 'microphone; camera');
    iframe.setAttribute('title', 'Chatbot Asesor de Vinos');

    // Ensamblar elementos
    container.appendChild(closeBtn);
    container.appendChild(iframe);

    // Variables de estado
    let isOpen = false;

    // Toggle chat
    function toggleChat() {
        isOpen = !isOpen;

        if (isOpen) {
            container.classList.add('open');
            button.classList.remove('wine-chatbot-pulse');

            // Vibración en móvil
            if (navigator.vibrate) {
                navigator.vibrate(10);
            }
        } else {
            container.classList.remove('open');
            button.classList.add('wine-chatbot-pulse');
        }
    }

    // Event listeners
    button.addEventListener('click', toggleChat);
    closeBtn.addEventListener('click', toggleChat);

    // Añadir al DOM cuando esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            document.body.appendChild(button);
            document.body.appendChild(container);
        });
    } else {
        document.body.appendChild(button);
        document.body.appendChild(container);
    }

    // Cerrar con tecla Escape
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && isOpen) {
            toggleChat();
        }
    });

    console.log('🍷 Widget Chatbot Calar Viejo cargado correctamente');

})();

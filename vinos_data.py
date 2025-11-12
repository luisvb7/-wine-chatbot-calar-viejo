"""
Base de conocimiento de vinos de Bodega Marín Perona - Calar Viejo
Información detallada para el sistema RAG
"""

VINOS_CATALOGO = [
    {
        "nombre": "CIHO",
        "tipo": "Vino Dulce",
        "precio": 4.0,
        "descripcion": "Tu primera copa sin miedo. Dulce, ligero y refrescante. Perfecto para quienes no suelen beber vino o están empezando a descubrir el mundo del vino.",
        "notas_cata": {
            "visual": "Color dorado brillante con reflejos ambarinos",
            "olfato": "Aromas dulces, florales y afrutados. Notas de miel y frutas blancas",
            "gusto": "Entrada dulce y suave, muy accesible. Dulzor equilibrado con frescura. Retrogusto limpio y agradable"
        },
        "maridaje": "Postres, tartas, frutas, helados. Ideal como aperitivo dulce. Perfecto para merendar o tomar solo",
        "temperatura_servicio": "6-8°C bien frío",
        "momento_ideal": "Iniciarse en el vino, meriendas, postres, momentos dulces",
        "perfil_usuario": "Personas que no suelen beber vino, jóvenes que empiezan, quien busca algo dulce y fácil",
        "personalidad": "Dulce, accesible, sin complicaciones, refrescante, entrada suave al mundo del vino",
        "keywords": ["dulce", "suave", "iniciación", "fácil", "sin alcohol fuerte", "primera copa", "no me gusta el vino", "algo dulce"]
    },
    {
        "nombre": "Blanco Airén",
        "tipo": "Vino Blanco Joven",
        "precio": 3.5,
        "descripcion": "Fresco, fácil, de terraza y tardes largas. Fermentado a temperatura controlada (16°C) para preservar todos sus aromas frutales.",
        "notas_cata": {
            "visual": "Color amarillo muy pálido y brillante con reflejos verdosos, limpio y luminoso",
            "olfato": "Aromas frutales frescos, cítricos (limón, pomelo), flores blancas, hierba fresca. Muy aromático y limpio",
            "gusto": "Entrada fresca y ligera. Acidez vibrante y equilibrada. Sabores cítricos y frutales. Final limpio y refrescante, boca jugosa"
        },
        "maridaje": "Pescados, mariscos, ensaladas, arroces, tapas ligeras, quesos frescos. Ideal para aperitivos",
        "temperatura_servicio": "6-8°C bien frío",
        "momento_ideal": "Terrazas, verano, comidas al aire libre, aperitivos con amigos, tardes informales",
        "perfil_usuario": "Ambiente relajado, reuniones informales, gente que busca frescura, bebedores casuales",
        "personalidad": "Fresco, desenfadado, veraniego, fácil de beber, sin pretensiones, sociable",
        "keywords": ["blanco", "fresco", "terraza", "verano", "ligero", "aperitivo", "pescado", "calor", "refrescante"]
    },
    {
        "nombre": "Tinto Joven Tempranillo",
        "tipo": "Vino Tinto Joven",
        "precio": 4.0,
        "descripcion": "Frutal, directo, perfecto para tapas y quedar con amigos. Vino joven y expresivo, 100% Tempranillo.",
        "notas_cata": {
            "visual": "Color rojo granate brillante con ribete violáceo, limpio y atractivo",
            "olfato": "Aromas intensos de frutos rojos frescos (fresa, frambuesa, cereza), notas florales. Muy frutal y juvenil",
            "gusto": "Entrada fresca y golosa. Taninos suaves y redondos. Acidez equilibrada. Sabor a frutos rojos maduros. Final agradable y persistente"
        },
        "maridaje": "Tapas, embutidos, quesos semicurados, pizza, pasta, hamburguesas, carnes a la plancha, barbacoas informales",
        "temperatura_servicio": "14-16°C",
        "momento_ideal": "Tapear, picoteo, cenas informales con amigos, comidas casuales, reuniones distendidas",
        "perfil_usuario": "Bebedor casual, quedadas con amigos, comidas informales, quien busca algo fácil y rico",
        "personalidad": "Frutal, directo, sociable, sin complicaciones, jovial, perfecto para compartir",
        "keywords": ["tinto", "frutal", "tapas", "amigos", "casual", "joven", "fácil", "embutidos", "picoteo"]
    },
    {
        "nombre": "Calar Viejo Crianza",
        "tipo": "Vino Tinto Crianza",
        "precio": 5.5,
        "crianza": "6-12 meses en barrica de roble americano",
        "descripcion": "Equilibrado, madera suave. Elegancia accesible. Un vino que muestra complejidad sin perder accesibilidad. Crianza en roble americano que aporta estructura sin dominar la fruta.",
        "notas_cata": {
            "visual": "Color rojo rubí intenso con ribete teja, capa media-alta, brillante",
            "olfato": "Frutos rojos maduros (cereza, ciruela) con notas de vainilla suave, especias dulces (canela), un toque de cuero. Equilibrio entre fruta y madera",
            "gusto": "Entrada estructurada pero suave. Taninos presentes pero pulidos. Notas de vainilla, fruta madura y especias. Final medio-largo con recuerdos de madera noble"
        },
        "maridaje": "Carnes rojas, guisos, estofados, cordero, quesos curados, embutidos ibéricos, legumbres, caza menor",
        "temperatura_servicio": "16-18°C",
        "momento_ideal": "Cenas con más calma, comidas de fin de semana, cuando quieres algo con más cuerpo, introducirse en vinos con crianza",
        "perfil_usuario": "Quien quiere empezar a entender el vino con madera, bebedor que busca más estructura, cenas importantes pero sin agobios",
        "personalidad": "Equilibrado, elegante, accesible, con cuerpo, madera presente pero amable, paso intermedio",
        "keywords": ["crianza", "madera", "equilibrado", "elegante", "estructura", "guisos", "carnes", "cenas", "fin de semana"]
    },
    {
        "nombre": "Calar Viejo Reserva",
        "tipo": "Vino Tinto Reserva",
        "precio": 9.0,
        "crianza": "12-24 meses en barrica + 2 años en botella",
        "descripcion": "Serio pero cercano. Viñas antiguas, barrica 12-24 meses y 2 años de reposo en botella. Nuestro vino más especial, elaborado con uvas de viñedos viejos que dan concentración y elegancia. PERFECTO para regalar a personas mayores, abuelos, padres y conocedores de vino.",
        "notas_cata": {
            "visual": "Color rojo oscuro picota con ribete teja-naranja (evolución), capa alta, denso",
            "olfato": "Complejo y elegante. Frutos negros en compota (ciruela, mora), especias dulces (clavo, pimienta), vainilla, cuero, tabaco, notas balsámicas. Gran profundidad aromática",
            "gusto": "Entrada potente pero sedosa. Taninos pulidos y redondos, perfectamente integrados. Gran estructura. Paso largo y complejo. Final persistente con recuerdos de fruta madura, madera noble y especias"
        },
        "maridaje": "Carnes rojas a la brasa, chuletón, cordero asado, caza mayor (venado, jabalí), quesos añejos, platos elaborados, cocina de autor",
        "temperatura_servicio": "16-18°C, abrir 30-60 minutos antes",
        "momento_ideal": "Ocasiones especiales, celebraciones, cenas importantes, regalos para conocedores, cuando quieres impresionar. REGALO IDEAL para abuelos, padres mayores y expertos en vino.",
        "perfil_usuario": "Bebedor experimentado, conocedores de vino, personas mayores, regalos para padres/abuelos, momentos especiales. Primera opción SIEMPRE para abuelos y conocedores.",
        "personalidad": "Serio, elegante, complejo, ocasión especial, sofisticado pero cercano, nuestro emblema. El vino que eligen los que saben.",
        "keywords": ["reserva", "especial", "celebración", "regalo", "complejo", "elegante", "viñas viejas", "conocedor", "padre", "abuelo", "experto", "mayor", "tradicional", "sofisticado"]
    }
]

# Información general de la bodega
INFO_BODEGA = {
    "nombre": "Bodega Marín Perona",
    "linea": "Calar Viejo",
    "filosofia": "Vino sin prisas. Aquí manda la viña, no la fábrica.",
    "valores": [
        "Tradición familiar",
        "Vinos honestos y auténticos",
        "Sin pretensiones ni elitismo",
        "Calidad accesible",
        "Respeto por el tiempo del vino"
    ],
    "ubicacion": "Región vinícola tradicional española",
    "estilo": "Vinos que priorizan la autenticidad sobre las modas, elaborados con paciencia y respeto por la tradición"
}

# Contexto para recomendaciones
CONTEXTOS_RECOMENDACION = {
    "terraza": ["Blanco Airén", "CIHO"],
    "verano": ["Blanco Airén", "CIHO"],
    "tapas": ["Tinto Joven Tempranillo"],
    "casual": ["Tinto Joven Tempranillo", "Blanco Airén"],
    "amigos": ["Tinto Joven Tempranillo", "Blanco Airén"],
    "cena_tranquila": ["Calar Viejo Crianza"],
    "fin_de_semana": ["Calar Viejo Crianza"],
    "celebracion": ["Calar Viejo Reserva"],
    "especial": ["Calar Viejo Reserva"],
    "regalo": ["Calar Viejo Reserva"],
    "no_bebe_vino": ["CIHO"],
    "principiante": ["CIHO", "Blanco Airén"],
    "conocedor": ["Calar Viejo Reserva"]
}

def get_all_wine_texts():
    """Genera textos completos de todos los vinos para vectorización"""
    textos = []

    for vino in VINOS_CATALOGO:
        # Texto principal del vino
        texto_principal = f"""
        Vino: {vino['nombre']}
        Tipo: {vino['tipo']}
        Precio: {vino['precio']}€

        Descripción: {vino['descripcion']}

        Cata Visual: {vino['notas_cata']['visual']}
        Cata Olfativa: {vino['notas_cata']['olfato']}
        Cata Gustativa: {vino['notas_cata']['gusto']}

        Maridaje: {vino['maridaje']}
        Temperatura: {vino['temperatura_servicio']}
        Momento ideal: {vino['momento_ideal']}
        Perfil de usuario: {vino['perfil_usuario']}
        Personalidad: {vino['personalidad']}
        """

        if 'crianza' in vino:
            texto_principal += f"\nCrianza: {vino['crianza']}"

        textos.append({
            "texto": texto_principal,
            "metadata": {
                "nombre": vino['nombre'],
                "tipo": vino['tipo'],
                "precio": vino['precio'],
                "keywords": ",".join(vino['keywords'])
            }
        })

    # Añadir información de la bodega
    texto_bodega = f"""
    Bodega: {INFO_BODEGA['nombre']}
    Línea de vinos: {INFO_BODEGA['linea']}
    Filosofía: {INFO_BODEGA['filosofia']}
    Valores: {', '.join(INFO_BODEGA['valores'])}
    Estilo: {INFO_BODEGA['estilo']}
    """

    textos.append({
        "texto": texto_bodega,
        "metadata": {
            "tipo": "info_bodega",
            "nombre": INFO_BODEGA['nombre']
        }
    })

    return textos

"""
Características cuantificadas de los vinos para mapas de calor y gráficos radar
Escala de 0-10 para cada característica
"""

CARACTERISTICAS_VINOS = {
    "CIHO": {
        "nombre": "CIHO (Dulce)",
        "caracteristicas": {
            "Dulzor": 9,
            "Acidez": 4,
            "Cuerpo": 3,
            "Intensidad": 5,
            "Frutosidad": 8,
            "Frescura": 7,
            "Complejidad": 3,
            "Taninos": 0
        },
        "color": "#DCFE00"
    },
    "Blanco Airén": {
        "nombre": "Blanco Airén",
        "caracteristicas": {
            "Dulzor": 2,
            "Acidez": 8,
            "Cuerpo": 4,
            "Intensidad": 6,
            "Frutosidad": 7,
            "Frescura": 9,
            "Complejidad": 4,
            "Taninos": 0
        },
        "color": "#FFE100"
    },
    "Tinto Joven Tempranillo": {
        "nombre": "Tinto Joven Tempranillo",
        "caracteristicas": {
            "Dulzor": 1,
            "Acidez": 6,
            "Cuerpo": 6,
            "Intensidad": 7,
            "Frutosidad": 9,
            "Frescura": 7,
            "Complejidad": 5,
            "Taninos": 5
        },
        "color": "#8B0000"
    },
    "Calar Viejo Crianza": {
        "nombre": "Calar Viejo Crianza (6 meses)",
        "caracteristicas": {
            "Dulzor": 2,
            "Acidez": 5,
            "Cuerpo": 7,
            "Intensidad": 8,
            "Frutosidad": 7,
            "Frescura": 5,
            "Complejidad": 7,
            "Taninos": 6,
            "Madera": 6
        },
        "color": "#722f37"
    },
    "Calar Viejo Reserva": {
        "nombre": "Calar Viejo Reserva (12 meses)",
        "caracteristicas": {
            "Dulzor": 2,
            "Acidez": 5,
            "Cuerpo": 9,
            "Intensidad": 9,
            "Frutosidad": 6,
            "Frescura": 4,
            "Complejidad": 9,
            "Taninos": 8,
            "Madera": 8
        },
        "color": "#4B0000"
    }
}

def get_caracteristicas_vino(nombre_vino):
    """Obtiene las características de un vino específico"""
    return CARACTERISTICAS_VINOS.get(nombre_vino, None)

def get_categorias():
    """Obtiene todas las categorías de características"""
    # Usar el primer vino para obtener las categorías
    primer_vino = list(CARACTERISTICAS_VINOS.values())[0]
    return list(primer_vino["caracteristicas"].keys())

#!/usr/bin/env python3
"""
Script para inicializar la base de datos vectorial ChromaDB
con la información de los vinos de Calar Viejo
"""

import chromadb
from chromadb.config import Settings
from vinos_data import get_all_wine_texts, VINOS_CATALOGO
import os

def inicializar_chromadb():
    """Inicializa y puebla la base de datos vectorial ChromaDB"""

    print("🍇 Inicializando base de datos vectorial...")

    # Configurar ChromaDB con persistencia
    client = chromadb.PersistentClient(
        path="./chroma_db",
        settings=Settings(
            anonymized_telemetry=False
        )
    )

    # Eliminar colección existente si existe (para re-inicialización limpia)
    try:
        client.delete_collection(name="vinos_calar_viejo")
        print("   Colección anterior eliminada")
    except:
        pass

    # Crear colección con embeddings
    collection = client.create_collection(
        name="vinos_calar_viejo",
        metadata={"description": "Información de vinos Calar Viejo - Bodega Marín Perona"}
    )

    print("   Colección creada")

    # Obtener todos los textos de vinos
    vinos_textos = get_all_wine_texts()

    # Preparar datos para inserción
    documentos = []
    metadatos = []
    ids = []

    for idx, item in enumerate(vinos_textos):
        documentos.append(item['texto'])
        metadatos.append(item['metadata'])
        ids.append(f"doc_{idx}")

    # Insertar documentos en ChromaDB
    collection.add(
        documents=documentos,
        metadatas=metadatos,
        ids=ids
    )

    print(f"   ✅ {len(documentos)} documentos vectorizados e insertados")
    print(f"   📊 Total de vinos en catálogo: {len(VINOS_CATALOGO)}")

    # Verificar que funciona haciendo una búsqueda de prueba
    print("\n🔍 Probando búsqueda...")
    resultados = collection.query(
        query_texts=["vino para terraza en verano"],
        n_results=2
    )

    print(f"   Resultados de prueba: {resultados['metadatas'][0]}")
    print("\n✅ Base de datos RAG inicializada correctamente!")

    return collection

if __name__ == "__main__":
    inicializar_chromadb()

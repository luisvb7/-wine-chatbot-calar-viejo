#!/usr/bin/env python3
"""
Script de prueba para verificar el funcionamiento del RAG
"""

import chromadb
from chromadb.config import Settings

def test_rag():
    """Prueba el sistema RAG con diferentes consultas"""

    print("🔍 Probando sistema RAG...\n")

    # Conectar con ChromaDB
    client = chromadb.PersistentClient(
        path="./chroma_db",
        settings=Settings(anonymized_telemetry=False)
    )

    collection = client.get_collection(name="vinos_calar_viejo")

    # Consultas de prueba
    consultas = [
        "vino para terraza en verano",
        "vino para regalar a mi padre",
        "algo dulce para alguien que no le gusta el vino",
        "vino para cena especial",
        "vino para tapas con amigos"
    ]

    for consulta in consultas:
        print(f"📝 Consulta: '{consulta}'")
        resultados = collection.query(
            query_texts=[consulta],
            n_results=2
        )

        print(f"   Vinos recomendados:")
        for i, metadata in enumerate(resultados['metadatas'][0], 1):
            nombre = metadata.get('nombre', 'N/A')
            precio = metadata.get('precio', 'N/A')
            print(f"   {i}. {nombre} - {precio}€")
        print()

    print("✅ Sistema RAG funcionando correctamente!")

if __name__ == "__main__":
    test_rag()

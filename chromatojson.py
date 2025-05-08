from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import json

# Chargement du modèle d'embedding
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Connexion à la base Chroma existante
chroma_db = Chroma(
    persist_directory="chroma_api_v2",
    embedding_function=embedding_model,
    collection_name="formations"
)

# Export de tous les documents et métadonnées
print("📦 Export des données depuis Chroma...")
data = chroma_db.get()

export_data = []
for doc, meta in zip(data["documents"], data["metadatas"]):
    export_data.append({
        "content": doc,
        "metadata": meta
    })

with open("data/export_faiss.json", "w", encoding="utf-8") as f:
    json.dump(export_data, f, ensure_ascii=False, indent=2)

print(f"✅ {len(export_data)} documents exportés dans export_faiss.json")

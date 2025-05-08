from components.initialize import initialize
import json
from langchain.schema import Document
# Initialisation
embedding_model, collection, api_collection = initialize()

def retrieve_memory(user_input, collection, embedding_model, max_memories=3):
    """Récupère les dernières conversations enregistrées (par date)"""
    all_data = collection.get(include=["documents", "metadatas"])

    documents = all_data["documents"]
    metadatas = all_data["metadatas"]

    # Trie tous les souvenirs par timestamp (du plus ancien au plus récent)
    sorted_docs = sorted(
        zip(documents, metadatas),
        key=lambda x: x[1].get("timestamp", "1970-01-01T00:00:00")
    )

    # Garde les N derniers (par défaut 3)
    selected_docs = sorted_docs[-max_memories:]

    formatted_memory = []
    for doc, meta in selected_docs:
        try:
            doc_str = doc[0] if isinstance(doc, tuple) else doc
            messages = json.loads(doc_str)
            lines = [f"{m['role'].capitalize()} : {m['content']}" for m in messages]
            formatted_memory.append("\n".join(lines))
        except Exception as e:
            print("❌ Erreur de parsing mémoire :", e)
            formatted_memory.append(str(doc))

    return formatted_memory  # Liste de str  # 


def retrieve_api_data(user_input, embedding_model, api_collection):
    """Recherche vectorielle dans Chroma et retourne une liste de documents"""
    vector = embedding_model.encode(user_input).tolist()
    results = api_collection.query(
        query_embeddings=[vector],
        n_results=10,
        include=["documents", "metadatas"],
        where={"source": "API"}
    )
    metadatas = results.get("metadatas", [[]])[0]
    documents = results.get("documents", [[]])[0]

    if not metadatas:
        print("❌ Aucun résultat trouvé.")
        return []

    docs = []
    for i, meta in enumerate(metadatas):
        doc_text = documents[i] if i < len(documents) else ""
        doc = Document(page_content=doc_text, metadata=meta)
        docs.append(doc)

    print(f"✅ {len(docs)} résultats récupérés avec métadonnées.")
    return docs

    

import json
from langchain_postgres.vectorstores import PGVector
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from sqlalchemy import create_engine
from tqdm import tqdm
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Connexion PostgreSQL
PGVECTOR_CONNECTION_STRING = "postgresql://postgres:admin@localhost:5432/chatbot_db?options=-csearch_path=public"
COLLECTION_NAME = "formations_pgvector"

# Modèle d'embedding
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Connexion SQLAlchemy
engine = create_engine(PGVECTOR_CONNECTION_STRING)

# Charger les documents JSON
with open("data/export_faiss.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Construire les objets Document
documents = [
    Document(page_content=item["content"], metadata=item["metadata"])
    for item in data
]

# Découper en chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50 )
documents = text_splitter.split_documents(documents)
print(f"📄 {len(documents)} chunks générés")

# Insertion dans PGVector
print("📥 Ajout des documents dans pgvector...")
BATCH_SIZE = 100
for i in tqdm(range(0, len(documents), BATCH_SIZE), desc="Insertion dans PGVector"):
    batch = documents[i:i + BATCH_SIZE]
    try:
        PGVector.from_documents(
            documents=batch,
            embedding=embedding_model,
            collection_name=COLLECTION_NAME,
            connection=engine
        )
    except Exception as e:
        print(f"❌ Erreur à l'insertion du batch {i//BATCH_SIZE + 1}: {e}")

print(f"✅ {len(documents)} chunks insérés dans la collection '{COLLECTION_NAME}'.")

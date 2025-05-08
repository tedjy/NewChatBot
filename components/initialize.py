from sentence_transformers import SentenceTransformer
import chromadb
from langchain_community.embeddings import HuggingFaceEmbeddings
#  Initialiser la base mémoire
def initialize():
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    db_conversations = chromadb.PersistentClient(path="./chroma_conversations")
    db_api = chromadb.PersistentClient(path="./chroma_api_v2")
    # collection pour les conversation
    collection = db_conversations.get_or_create_collection("chat_memory")
    # collection pour les données de l'api
    api_collection = db_api.get_or_create_collection("formations")

    # 🔹 On retourne tout ce dont on a besoin
    return embedding_model, collection, api_collection

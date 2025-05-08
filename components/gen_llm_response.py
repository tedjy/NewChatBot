from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from sqlalchemy import create_engine, text
import streamlit as st
import json

# Configuration base de données PostgreSQL avec PGVector
PGVECTOR_CONNECTION_STRING = "postgresql://postgres:admin@localhost:5432/chatbot_db?options=-csearch_path=public"
COLLECTION_NAME = "formations_pgvector"

# Initialiser les embeddings (en mémoire partagée si possible)
if "embedding_model_shared" not in st.session_state:
    st.session_state.embedding_model_shared = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
embedding_model_shared = st.session_state.embedding_model_shared

# Connexion PostgreSQL
engine = create_engine(PGVECTOR_CONNECTION_STRING)

# Niveaux hiérarchiques simplifiés
HIERARCHIE_DIPLOMES = ["cap", "bac", "bts", "dut", "but", "licence", "master", "doctorat"]

# Chargement des villes et domaines depuis fichiers (à préparer séparément)
try:
    with open("data/villes_france.json", "r", encoding="utf-8") as f:
        VILLES_FRANCE = json.load(f)
except:
    VILLES_FRANCE = []

try:
    with open("data/domaines_formation.json", "r", encoding="utf-8") as f:
        DOMAINES_FORMATION = json.load(f)
except:
    DOMAINES_FORMATION = []

# Prompt personnalisé
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""### Instructions :
Tu es un assistant d’orientation scolaire. Tu aides l'utilisateur à trouver une formation ou un établissement.

Pose des questions si l'utilisateur n'a pas donné son âge, sa ville, ou son dernier diplôme. Quand ces infos sont connues, propose uniquement des formations d'un niveau supérieur à son dernier diplôme.

### Contexte :
{context}

### Question :
{question}

### Réponse :"""
)

def search_pgvector_similar_documents(query: str, k: int = 10):
    query_embedding = embedding_model_shared.embed_query(query)
    if len(query_embedding) != 384:
        raise ValueError(f"⚠️ Dimensions incorrectes : attendu 384, obtenu {len(query_embedding)}")

    embedding_str = "[" + ",".join([f"{x:.6f}" for x in query_embedding]) + "]"
    sql = text("""
        SELECT document
        FROM langchain_pg_embedding
        WHERE collection_id = (
            SELECT uuid FROM langchain_pg_collection WHERE name = :collection_name LIMIT 1
        )
        ORDER BY embedding <-> :embedding
        LIMIT :k
    """)
    with engine.connect() as conn:
        results = conn.execute(sql, {
            "collection_name": COLLECTION_NAME,
            "embedding": embedding_str,
            "k": k
        }).fetchall()
    return results

def generate_llm_response(message: str, model_fn):
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

    st.session_state.conversation_history.append(message)
    full_context = "\n".join([f"Utilisateur : {msg}" for msg in st.session_state.conversation_history])

    # Requête enrichie explicitement pour guider la recherche vectorielle
    search_query = full_context + "\nFiltrer uniquement les formations correspondant à la ville, au domaine et au niveau demandé."
    results = search_pgvector_similar_documents(search_query, k=20)

    # Filtrage dynamique par domaine ou ville contenus dans la base de référence
    def correspond_aux_criteres(doc):
        contenu = doc[0].lower()
        return any(v.lower() in contenu for v in VILLES_FRANCE) and any(d.lower() in contenu for d in DOMAINES_FORMATION)

    filtered_results = [r for r in results if correspond_aux_criteres(r)]

    retrieved_context = "\n".join(f"- {row[0]}" for row in filtered_results) if filtered_results else "Aucun résultat pertinent trouvé."

    final_prompt = prompt_template.format(context=retrieved_context, question=full_context)
    response = model_fn(final_prompt)

    return response if response.strip() else "❌ Réponse vide."

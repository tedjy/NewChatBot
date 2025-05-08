import asyncio
import sys
from components.interface import interface
from langchain_community.llms import Ollama



# Initialisation Ollama (modèle local)
model_fn = Ollama(model="mistral")

# Correction pour Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# st.write("💾 Utilisation de la mémoire RAG")

# Initialisation mémoire + données API
# embedding_model, collection, api_collection = initialize()

# Interface Streamlit
interface(model_fn)
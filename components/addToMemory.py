import json
from components.initialize import initialize
import datetime 
import uuid 
import re
# Initialisation
embedding_model, collection, api_collection = initialize()


def add_to_memory(user_input, response, embedding_model, collection, role="assistant", source="conversation"):
    message_pair = [
        {"role": "user", "content": user_input},
        {"role": role, "content": response}
    ]
    document_json = json.dumps(message_pair, ensure_ascii=False)
    vector = embedding_model.embed_query(document_json)
    memory_id = str(uuid.uuid4())
    timestamp = datetime.datetime.now().isoformat()

    print(f"📝 Ajout en mémoire : {document_json}")

    collection.add(
        documents=[document_json],
        embeddings=[vector],
        metadatas=[{
            "source": source,
            "timestamp": timestamp
        }],
        ids=[memory_id]
    )

    nb_conversations = len(collection.get()['ids']) if collection.get() and 'ids' in collection.get() else 0
    print(f"📌 Nombre total de conversations enregistrées : {nb_conversations}")
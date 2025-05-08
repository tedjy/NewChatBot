# from components.initialize import initialize
# import json

# def exporter_api_chroma_en_json(api_collection, fichier_sortie="./jsonData/chroma_api.json"):
#     # On récupère tous les documents et métadonnées de la collection
#     data = api_collection.get(include=["documents", "metadatas"])

#     resultat = []
#     if data and "metadatas" in data:
#         for meta in data["metadatas"]:
#             item = {
#                 "Formation": meta.get("Formation", ""),
#                 "Type": meta.get("Type", ""),
#                 "Durée": meta.get("Durée", ""),
#                 "Niveau de sortie": meta.get("Niveau de sortie", ""),
#                 "Certification": meta.get("Certification", ""),
#                 "Établissement": meta.get("Établissement", ""),
#                 "Ville": meta.get("Ville", ""),
#                 "Code postal": meta.get("Code postal", ""),
#                 "Plus d'infos": meta.get("Plus d'infos", ""),
#                 "Domaine": meta.get("Domaine", "")
#             }
#             resultat.append(item)

#     with open(fichier_sortie, "w", encoding="utf-8") as f:
#         json.dump(resultat, f, ensure_ascii=False, indent=4)

#     print(f"✅ Export terminé : {len(resultat)} formations enregistrées dans {fichier_sortie}")



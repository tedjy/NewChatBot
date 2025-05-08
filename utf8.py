with open("data/export_faiss.json", "r", encoding="latin1") as f:
    content = f.read()

with open("data/export_faiss_utf8.json", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ export_faiss_utf8.json encodé en UTF-8")
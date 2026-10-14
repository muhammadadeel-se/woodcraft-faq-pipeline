import sqlite3
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

print("Loading FAQ data from SQLite database...")
conn = sqlite3.connect("faq.db")
cursor = conn.cursor()
cursor.execute("SELECT id, answer FROM faq")
rows = cursor.fetchall()
conn.close()

faq_ids = [row[0] for row in rows]
answers = [row[1] for row in rows]

print(f"Loaded {len(answers)} FAQ entries. Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Computing embeddings...")
embeddings = model.encode(answers, show_progress_bar=True)
embeddings = np.array(embeddings).astype("float32")

# Normalize vectors for cosine similarity search
faiss.normalize_L2(embeddings)
dimension = embeddings.shape[1]

# Create FAISS Index
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

# Save index and ID mapping
faiss.write_index(index, "faiss_index.bin")
with open("faq_ids.pkl", "wb") as f:
    pickle.dump(faq_ids, f)

print(f"Successfully built and saved FAISS index! Total vectors: {index.ntotal}")
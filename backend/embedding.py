import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed(texts):
    """
    Convert list of texts into embeddings
    """
    return model.encode(texts, show_progress_bar=True)


if __name__ == "__main__":

    text_path = r"C:\Users\Anabia\Downloads\student-handbook-gpt\backend\sample_text.txt"

    print("📄 Loading text file...")
    with open(text_path, "r", encoding="utf-8") as f:
        texts = [line.strip() for line in f.readlines() if line.strip()]

    print(f"✅ Total Q&A lines loaded: {len(texts)}")

    print("⚙️ Generating embeddings...")
    embeddings = embed(texts).astype("float32")

    print("💾 Saving embeddings...")
    np.save("embeddings.npy", embeddings)

    print("⚙️ Building FAISS index...")
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    print("💾 Saving FAISS index...")
    faiss.write_index(index, "faiss.index")

    print("💾 Saving text mapping...")
    with open("texts.txt", "w", encoding="utf-8") as f:
        for t in texts:
            f.write(t + "\n")

    print("✅ DONE! Embeddings and FAISS index created successfully.")

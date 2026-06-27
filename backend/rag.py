import os
import faiss
import numpy as np
from .embedding import embed
from sklearn.metrics.pairwise import cosine_similarity


class RAGPipeline:
    def __init__(
        self,
        texts_path="texts.txt",
        index_path="faiss.index",
        embeddings_path="embeddings.npy",
        similarity_threshold=0.5,  # Minimum similarity to consider
    ):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        self.texts_path = os.path.join(base_dir, texts_path)
        self.index_path = os.path.join(base_dir, index_path)
        self.embeddings_path = os.path.join(base_dir, embeddings_path)
        self.similarity_threshold = similarity_threshold

        # ----------------------------
        # Load texts
        # ----------------------------
        if not os.path.exists(self.texts_path):
            raise FileNotFoundError(f"Missing texts file: {self.texts_path}")

        print("📄 Loading texts...")
        with open(self.texts_path, "r", encoding="utf-8") as f:
            self.texts = [line.strip() for line in f if line.strip()]

        if not self.texts:
            raise ValueError("texts.txt is empty!")

        print(f"✅ Loaded {len(self.texts)} text chunks")

        # ----------------------------
        # Load embeddings
        # ----------------------------
        if not os.path.exists(self.embeddings_path):
            raise FileNotFoundError("embeddings.npy not found. Run embedding.py first!")

        print("📦 Loading embeddings...")
        self.embeddings = np.load(self.embeddings_path).astype("float32")

        # ----------------------------
        # Load FAISS index
        # ----------------------------
        if not os.path.exists(self.index_path):
            raise FileNotFoundError("faiss.index not found. Run embedding.py first!")

        print("📌 Loading FAISS index...")
        self.index = faiss.read_index(self.index_path)

        print("✅ RAG pipeline ready")

    # ----------------------------
    # Search with similarity check
    # ----------------------------
    def search(self, query, k=3):
        if not query.strip():
            return []

        # Embed the query
        q_emb = embed([query]).astype("float32")

        # FAISS search
        distances, indices = self.index.search(q_emb, k)

        results = []
        for idx in indices[0]:
            if 0 <= idx < len(self.texts):
                candidate = self.texts[idx]
                # Cosine similarity check
                sim = cosine_similarity(
                    q_emb, self.embeddings[idx].reshape(1, -1)
                )[0][0]
                if sim >= self.similarity_threshold:
                    results.append(candidate)

        return results


# ----------------------------
# Test
# ----------------------------
if __name__ == "__main__":
    rag = RAGPipeline(similarity_threshold=0.5)
    results = rag.search("When was SZABIST established?")

    print("\n🔍 Search Results:")
    for r in results:
        print("-", r)

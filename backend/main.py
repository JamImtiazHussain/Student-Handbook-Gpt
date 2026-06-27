import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from .rag import RAGPipeline

app = FastAPI(title="Student Handbook GPT")

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- INIT RAG ----------------
print("🔍 Initializing RAG pipeline...")
rag = RAGPipeline()
print("✅ RAG ready")

# ---------------- FRONTEND ----------------
frontend_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "frontend")
)

app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def root():
    return FileResponse(os.path.join(frontend_path, "index.html"))

# ---------------- REQUEST MODEL ----------------
class Question(BaseModel):
    question: str

# ---------------- ASK ENDPOINT ----------------
@app.post("/ask")
def ask(data: Question):
    query = data.question.strip()
    print("❓ Question:", query)

    if not query:
        return {"answer": "Please ask a valid question."}

    # ---- RAG search ----
    results = rag.search(query, k=3)

    if not results:
        return {"answer": "Sorry, I could not find this information in the handbook."}

    best = results[0]

    # If Q/A format exists → return answer only
    if "A:" in best:
        return {"answer": best.split("A:", 1)[1].strip()}

    return {"answer": best}

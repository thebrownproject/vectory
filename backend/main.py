from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from adapters import PineconeAdapter
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Vectory API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Vectory API - PDF to Vector Pipeline"}

@app.get("/api/health")
def health_check():
    try:
        adapter = PineconeAdapter()
        pinecone_status = adapter.health_check()
        return {"status": "ok", "pinecone_connected": pinecone_status}
    except Exception as e:
        return {"status": "ok", "pinecone_connected": False, "error": str(e)}

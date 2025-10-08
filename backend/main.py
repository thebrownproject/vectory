from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from adapters import PineconeAdapter
from dotenv import load_dotenv
from routers import upload

# Load environment variables from .env file (API keys, Pinecone config)
load_dotenv()

app = FastAPI(title="Vectory API", version="0.1.0")

# Include routers
app.include_router(upload.router)

# Configure CORS for local development
# Allows Next.js frontend (localhost:3000) to make requests to FastAPI (localhost:8000)
# In production, replace with specific domain or use environment variable
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
    """
    Health check endpoint - verifies API is running and Pinecone connection works.

    Used by monitoring tools and frontend to check backend status.
    Returns 200 even if Pinecone fails (graceful degradation).
    """
    try:
        adapter = PineconeAdapter()
        pinecone_status = adapter.health_check()
        return {"status": "ok", "pinecone_connected": pinecone_status}
    except Exception as e:
        # Return 200 with error details - don't crash the health check
        return {"status": "ok", "pinecone_connected": False, "error": str(e)}

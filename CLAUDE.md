# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Vectory is a lightweight PDF-to-vector ingestion pipeline. It accepts PDF uploads, processes them into chunks, generates embeddings via OpenAI, and stores vectors in Pinecone. This is a proof-of-concept focused on simplicity - not a production application.

**Query interface**: Vectors are queried separately via Claude Desktop MCP (not part of this codebase).

## Architecture

### Two-Tier Structure
- **Frontend**: Next.js 15 (App Router) on localhost:3000 - handles file uploads and displays processing status
- **Backend**: FastAPI on localhost:8000 - handles PDF processing, embeddings, and vector storage

### Processing Pipeline
1. User uploads PDF → Frontend sends to FastAPI `/api/upload`
2. Backend extracts text (PyPDF2/pdfplumber)
3. Backend chunks text using LangChain's RecursiveCharacterTextSplitter (1000 chars, 200 overlap)
4. Backend generates embeddings (OpenAI `text-embedding-3-small`, 1536 dimensions)
5. Backend upserts to Pinecone with metadata (filename, page number, chunk index, timestamp)
6. Backend returns stats → Frontend displays confirmation

### Vector DB Adapter Pattern
The backend uses an adapter pattern to abstract vector database operations:

- **Base class**: `backend/adapters/base_adapter.py` - defines `upsert()` and `health_check()` interface
- **Current implementation**: `backend/adapters/pinecone_adapter.py`
- **Future implementations**: Chroma, Supabase, Weaviate (swap via `VECTOR_DB_PROVIDER` env var)

This allows switching vector databases with minimal code changes.

## Development Commands

### Backend (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev  # Runs on localhost:3000
```

## Environment Configuration

### Backend `.env`
```
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=vectory
VECTOR_DB_PROVIDER=pinecone  # For adapter switching
```

### Frontend `.env.local`
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## API Contract

### POST /api/upload
- **Input**: multipart/form-data with .pdf file(s)
- **Output**: `{"success": true, "files_processed": 1, "results": [{"filename": "doc.pdf", "chunks_created": 45, "vectors_stored": 45, "namespace": "doc-uuid-12345"}]}`
- **Errors**: 400 (invalid file), 422 (extraction failure), 503 (API/DB failure)

### GET /api/health
- **Output**: `{"status": "ok", "pinecone_connected": true}`

## Metadata Schema
Each vector in Pinecone includes:
```json
{
  "filename": "document.pdf",
  "page_number": 3,
  "chunk_index": 12,
  "upload_timestamp": "2025-10-05T14:30:00Z",
  "total_chunks": 45,
  "text": "original chunk text..."
}
```

## Code Philosophy

**This is a POC. Prioritize simplicity over enterprise patterns.**

- Write minimal, readable code with direct implementations
- Keep functions small and focused
- Only add dependencies that are truly essential (question every `pip install` / `npm install`)
- Use LangChain ONLY for text splitting (it's good at this specific task)
- Avoid over-abstraction, elaborate folder structures, and "just in case" features
- Goal: Someone should read the entire codebase in 15 minutes and understand it

**Exception to simplicity**: The vector DB adapter pattern adds intentional abstraction to support future database swaps without refactoring.

## Task Tracking

**Always check `tasks.md` when starting work.** It contains the complete development roadmap broken into phases. Mark tasks complete with `[x]` as you finish them.

Current development follows this sequence:
1. Setup & Configuration
2. Vector DB Adapter (abstraction layer)
3. PDF Processing (extraction + chunking)
4. Embeddings (OpenAI integration)
5. Upload Endpoint (full pipeline)
6. Frontend Upload Interface
7. Error Handling & Feedback
8. Testing & Validation
9. Documentation

## Key Constraints

- **Local development only** - no deployment infrastructure
- **Support PDFs up to 50MB**
- **Processing target: <30 seconds** per typical PDF
- **Text extraction accuracy: >95%** for digital PDFs (no OCR support)
- **OpenAI embedding model**: `text-embedding-3-small` (1536 dimensions)
- **Chunking parameters**: 1000 characters, 200 character overlap

## Out of Scope

- Authentication/user accounts
- Query interface (handled by Claude Desktop MCP)
- Chat history
- Document management (delete, update operations)
- OCR for scanned PDFs
- Deployment configuration

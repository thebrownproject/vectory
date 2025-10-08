# Vectory

> A lightweight PDF-to-vector ingestion pipeline for building searchable document knowledge bases

[![Next.js](https://img.shields.io/badge/Next.js-15-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.118-009688)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB)](https://www.python.org/)

## Overview

Vectory is a full-stack web application that transforms PDF documents into searchable vector embeddings. Upload PDFs through a clean drag-and-drop interface, and Vectory automatically extracts text, chunks content intelligently, generates embeddings via OpenAI, and stores vectors in Pinecone for semantic search.

This is a proof-of-concept demonstrating modern document ingestion architecture with an adapter pattern for vector database portability.

## Features

- **Drag-and-drop PDF upload** with real-time processing feedback
- **Intelligent text chunking** (1000 chars, 200 char overlap) using LangChain
- **OpenAI embeddings** via `text-embedding-3-small` (1536 dimensions)
- **Vector database adapter pattern** for easy swapping between Pinecone, Chroma, Supabase, or Weaviate
- **Rich metadata tracking** (filename, page number, chunk index, timestamp)
- **Comprehensive error handling** with user-friendly messages
- **Clean architecture** with service layer separation and type-safe TypeScript

## Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐      ┌──────────┐
│   Next.js   │─────▶│   FastAPI    │─────▶│   OpenAI    │      │ Pinecone │
│   Frontend  │      │   Backend    │      │  Embeddings │      │  Vectors │
│ (localhost  │◀─────│ (localhost   │      └─────────────┘      └──────────┘
│    :3000)   │      │    :8000)    │              │                   ▲
└─────────────┘      └──────────────┘              │                   │
                             │                     └───────────────────┘
                             ▼                       Vector Upsert
                     ┌──────────────┐
                     │ PDF Processor│
                     │  (pypdf +    │
                     │  LangChain)  │
                     └──────────────┘
```

## Tech Stack

### Frontend
- **Next.js 15** (App Router) - React framework with server components
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **react-dropzone** - File upload handling
- **Lucide React** - Icon library

### Backend
- **FastAPI** - High-performance Python web framework
- **pypdf** - PDF text extraction
- **LangChain** - Text splitting utilities
- **OpenAI Python SDK** - Embedding generation
- **Pinecone** - Vector database storage

## Getting Started

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **OpenAI API key** ([Get one here](https://platform.openai.com/api-keys))
- **Pinecone account** ([Sign up free](https://www.pinecone.io/))
  - Create an index named `vectory` with 1536 dimensions (cosine metric)

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/thebrownproject/vectory.git
cd vectory
```

**2. Backend setup**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**3. Frontend setup**

```bash
cd ../frontend
npm install
```

### Configuration

**Backend environment variables** (`backend/.env`):

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your credentials
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=vectory
VECTOR_DB_PROVIDER=pinecone
```

**Frontend environment variables** (`frontend/.env.local`):

```bash
# Copy the example file
cp .env.local.example .env.local

# Default value (no changes needed for local dev)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Usage

**Start the backend** (from `backend/` directory):

```bash
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

**Start the frontend** (from `frontend/` directory):

```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

**Upload a PDF:**

1. Navigate to `http://localhost:3000`
2. Drag and drop a PDF file (or click to browse)
3. Click "Upload"
4. View processing results (chunks created, vectors stored, namespace)
5. Query vectors separately via Claude Desktop MCP or Pinecone console

## Project Structure

```
vectory/
├── frontend/                  # Next.js application
│   ├── app/
│   │   └── page.tsx          # Main upload interface
│   ├── components/
│   │   ├── FileUpload.tsx    # Drag-drop component
│   │   └── StatusDisplay.tsx # Processing feedback
│   └── lib/
│       └── api.ts            # API service layer
│
├── backend/                   # FastAPI application
│   ├── main.py               # App entry point
│   ├── routers/
│   │   └── upload.py         # Upload endpoint
│   ├── services/
│   │   ├── pdf_processor.py  # PDF extraction & chunking
│   │   └── embeddings.py     # OpenAI embedding generation
│   ├── adapters/
│   │   ├── base_adapter.py   # Abstract vector DB interface
│   │   └── pinecone_adapter.py # Pinecone implementation
│   └── tests/                # Test scripts
│
├── tasks.md                  # Development roadmap
├── prd.md                    # Product requirements
└── README.md
```

## API Endpoints

### `POST /api/upload`

Upload and process PDF files into vector embeddings.

**Request:** `multipart/form-data` with PDF file(s)

**Response:**
```json
{
  "success": true,
  "files_processed": 1,
  "results": [
    {
      "filename": "document.pdf",
      "chunks_created": 45,
      "vectors_stored": 45,
      "namespace": "document.pdf-a1b2c3d4"
    }
  ]
}
```

**Error codes:**
- `400` - Invalid file type (non-PDF)
- `422` - PDF extraction failure (corrupted file or no text)
- `503` - Service failure (OpenAI API or Pinecone error)

### `GET /api/health`

Check backend and Pinecone connection status.

**Response:**
```json
{
  "status": "ok",
  "pinecone_connected": true
}
```

## Vector Database Adapter Pattern

Vectory uses an adapter pattern to abstract vector database operations, making it easy to swap providers without refactoring application code.

**Current implementation:** Pinecone
**Planned support:** Chroma, Supabase Vector, Weaviate

To switch providers, simply:
1. Implement the `VectorDBAdapter` interface in `adapters/`
2. Update `VECTOR_DB_PROVIDER` in `.env`

## Development Notes

- **Text chunking:** 1000 characters with 200 character overlap via LangChain's RecursiveCharacterTextSplitter
- **Embedding model:** OpenAI `text-embedding-3-small` (1536 dimensions)
- **Namespace format:** `{filename}-{uuid}` to support re-uploading the same file
- **Metadata schema:** Includes filename, page number, chunk index, timestamp, and original text

## Future Enhancements

- Multi-tenant architecture with user authentication
- Support for Word docs, Excel, and images (OCR)
- Direct integrations with Notion, Google Drive, Confluence
- Usage analytics and cost tracking
- Query interface (currently handled separately via Claude Desktop MCP)

## License

MIT License - see LICENSE file for details

## Author

Built by [Fraser Brown](https://github.com/thebrownproject) as a portfolio project demonstrating full-stack development, clean architecture, and modern AI integration patterns.

---

**⭐ If you found this project useful, please consider starring it on GitHub!**

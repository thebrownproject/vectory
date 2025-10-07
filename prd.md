# Vectory - PDF Vector Ingestion Pipeline PRD

## Project Goal
Build a lightweight web app that accepts PDF uploads, processes them into chunks, generates embeddings, and stores them in Pinecone. Users will query the vectors separately via Claude Desktop MCP.

---

## User Stories & Functional Requirements

### US1: Upload PDFs
**As a user, I want to upload PDF files to be processed and stored in my vector database**

- **FR1.1**: Drag-and-drop file upload component (accept .pdf only)
- **FR1.2**: Support single or multiple file uploads
- **FR1.3**: Display upload progress/status for each file
- **FR1.4**: Show success confirmation with file name and chunk count

### US2: Document Processing
**As a system, I need to process PDFs into vector embeddings**

- **FR2.1**: Extract text from uploaded PDFs
- **FR2.2**: Split text into chunks (1000 characters, 200 character overlap)
- **FR2.3**: Generate embeddings using OpenAI text-embedding-3-small
- **FR2.4**: Include metadata: filename, page number, timestamp, chunk index

### US3: Vector Storage
**As a system, I need to store vectors in Pinecone with portability in mind**

- **FR3.1**: Upsert vectors to Pinecone with metadata
- **FR3.2**: Use abstraction layer (adapter pattern) for vector DB operations
- **FR3.3**: Support future swap to Chroma/Supabase/Weaviate without code refactor
- **FR3.4**: Namespace documents by upload session or filename

### US4: Processing Feedback
**As a user, I want to see what's happening during processing**

- **FR4.1**: Real-time status updates (uploading → extracting → embedding → storing)
- **FR4.2**: Error handling with clear messages (failed upload, processing error)
- **FR4.3**: Display total vectors created per document

---

## Tech Stack

### Frontend
- Next.js 15 (App Router)
- TypeScript
- Tailwind CSS
- React Hook Form (file upload handling)

### Backend
- FastAPI 0.115+
- Python 3.11+
- PyPDF2 or pdfplumber (PDF text extraction)
- LangChain (text splitting utilities)
- OpenAI API (embeddings)
- Pinecone Python SDK

### Development
- Local development only (no deployment required)
- Frontend: localhost:3000
- Backend: localhost:8000

---

## Code Philosophy - KEEP IT LIGHTWEIGHT

**This is a proof of concept. Prioritize simplicity over enterprise patterns.**

### DO:
✅ Write minimal, readable code  
✅ Use direct implementations over abstractions  
✅ Keep functions small and focused  
✅ Inline simple logic (don't create utility files for 3-line functions)  
✅ Use essential error handling only  
✅ Minimal comments (code should be self-explanatory)  

### DON'T:
❌ Over-abstract with unnecessary layers  
❌ Create elaborate folder structures  
❌ Add features "just in case"  
❌ Write extensive docstrings for obvious functions  
❌ Build complex middleware/decorators  
❌ Add verbose logging everywhere  
❌ Install libraries for things you can do in 10 lines of native code  

### Dependencies:
**Use only essential packages. Every dependency adds complexity.**

- If native Python/JavaScript can do it simply, don't add a library
- Prefer standard library over third-party packages when possible
- Question every `npm install` or `pip install`
- Only use LangChain for text splitting (it's good at this)
- Avoid helper libraries for trivial tasks

**Goal:** Someone should be able to read the entire codebase in 15 minutes and understand exactly what it does. Minimal dependencies = easier maintenance.

---

## File Structure

```
vectory/
├── frontend/                  # Next.js application
│   ├── app/
│   │   ├── page.tsx          # Main upload interface
│   │   └── api/
│   │       └── upload/
│   │           └── route.ts  # Proxy to FastAPI
│   ├── components/
│   │   ├── FileUpload.tsx    # Drag-drop component
│   │   └── StatusDisplay.tsx # Processing status
│   ├── package.json
│   └── tailwind.config.js
│
├── backend/                   # FastAPI application
│   ├── main.py               # FastAPI app entry point
│   ├── routers/
│   │   └── upload.py         # Upload endpoint
│   ├── services/
│   │   ├── pdf_processor.py  # PDF text extraction
│   │   ├── embeddings.py     # OpenAI embedding generation
│   │   └── vector_store.py   # Vector DB adapter interface
│   ├── adapters/
│   │   ├── pinecone_adapter.py  # Pinecone implementation
│   │   └── base_adapter.py      # Abstract base class
│   ├── tests/                # Test scripts
│   │   ├── test_adapter.py       # Pinecone adapter tests
│   │   ├── test_embeddings.py    # Embeddings service tests
│   │   ├── test_pdf_processor.py # PDF processing tests
│   │   └── test_upload_endpoint.py # Upload endpoint tests
│   ├── requirements.txt
│   └── .env                  # API keys
│
└── README.md                 # Setup instructions
```

---

## API Endpoints

### POST /api/upload
**Request:**
- Content-Type: multipart/form-data
- Body: PDF file(s)

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
      "namespace": "doc-uuid-12345"
    }
  ]
}
```

### GET /api/health
**Response:**
```json
{
  "status": "ok",
  "pinecone_connected": true
}
```

---

## Environment Variables

### Backend (.env)
```
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=vectory
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Vector DB Adapter Pattern

**Base Interface:**
```python
class VectorDBAdapter(ABC):
    @abstractmethod
    def upsert(self, vectors, metadata, namespace)
    
    @abstractmethod
    def health_check()
```

**Implementations:**
- PineconeAdapter (current)
- ChromaAdapter (future)
- SupabaseAdapter (future)
- WeaviateAdapter (future)

**Configuration:** Use environment variable `VECTOR_DB_PROVIDER=pinecone` to switch adapters

---

## Processing Flow

1. User uploads PDF via frontend
2. Frontend sends file to FastAPI `/api/upload`
3. Backend extracts text from PDF
4. Backend chunks text (RecursiveCharacterTextSplitter)
5. Backend generates embeddings via OpenAI API
6. Backend upserts to Pinecone with metadata
7. Backend returns success response with stats
8. Frontend displays confirmation

**Error Handling:**
- Invalid file type → 400 error
- PDF extraction failure → 422 error
- Embedding API failure → 503 error (retry logic)
- Pinecone upsert failure → 503 error

---

## Metadata Schema

Each vector stored in Pinecone includes:
```json
{
  "filename": "building_survey_rfi.pdf",
  "page_number": 3,
  "chunk_index": 12,
  "upload_timestamp": "2025-10-05T14:30:00Z",
  "total_chunks": 45,
  "text": "original chunk text..."
}
```

---

## MVP Scope

### In Scope
✅ Single/multi PDF upload  
✅ Text extraction and chunking  
✅ OpenAI embeddings  
✅ Pinecone storage  
✅ Processing status feedback  
✅ Vector DB adapter abstraction  

### Out of Scope (Future)
❌ Authentication/user accounts  
❌ Query interface (use Claude Desktop MCP)  
❌ Chat history  
❌ Deployment configuration  
❌ Document management (delete, update)  
❌ OCR for scanned PDFs  

---

## Success Criteria

- Upload PDF → vectors in Pinecone in <30 seconds
- Support PDFs up to 50MB
- Accurate text extraction (>95% for digital PDFs)
- Clean error messages for all failure modes
- Able to swap vector DB in <10 lines of code change

---

## Future Considerations (Post-POC)

**SaaS Pivot Potential:**
- Multi-tenant with user accounts
- Support for Word docs, Excel, images (OCR)
- Direct integrations: Notion, Google Drive, Confluence
- Multiple vector DB destinations per user
- Usage analytics and cost tracking
- API keys for programmatic access

**Use Case:**
"Vectory: Your document ingestion pipeline. Upload once, query anywhere."
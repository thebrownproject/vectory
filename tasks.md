# Vectory - Development Tasks

## Project Status: Phase 5 Complete ✅
**Current Phase**: Phase 6 - Frontend Upload Interface

---

## Phase 1: Project Setup & Configuration ✅

- [x] **T1.1**: Initialize backend FastAPI project structure
  - Create `backend/` directory
  - Set up `main.py`, `requirements.txt`
  - Create folder structure: `routers/`, `services/`, `adapters/`

- [x] **T1.2**: Initialize frontend Next.js project
  - Create Next.js 15 app with TypeScript and Tailwind
  - Configure to run on localhost:3000
  - Set up basic page structure

- [x] **T1.3**: Configure environment variables
  - Create `backend/.env` with Pinecone and OpenAI keys
  - Create `frontend/.env.local` with API URL
  - Add `.env` files to `.gitignore`

- [x] **T1.4**: Install and verify backend dependencies
  - FastAPI, uvicorn, python-multipart
  - pypdf (replaced PyPDF2)
  - LangChain text splitters
  - OpenAI SDK
  - Pinecone SDK
  - python-dotenv

- [x] **T1.5**: Configure CORS in FastAPI for local development
  - Allow localhost:3000 origin
  - Configure for multipart/form-data

---

## Phase 2: Backend Core - Vector DB Adapter (FR3.1, FR3.2, FR3.3) ✅

- [x] **T2.1**: Create base vector DB adapter interface
  - File: `backend/adapters/base_adapter.py`
  - Abstract methods: `upsert()`, `health_check()`
  - Define method signatures with type hints

- [x] **T2.2**: Implement Pinecone adapter
  - File: `backend/adapters/pinecone_adapter.py`
  - Implement `upsert()` with namespace support
  - Implement `health_check()` to verify connection
  - Handle Pinecone-specific errors

- [x] **T2.3**: Test Pinecone connection
  - Create simple health check endpoint
  - Verify Pinecone index exists and is accessible
  - Test upsert with sample vector

---

## Phase 3: Backend Core - PDF Processing (FR2.1, FR2.2) ✅

- [x] **T3.1**: Implement PDF text extraction service
  - File: `backend/services/pdf_processor.py`
  - Extract text from uploaded PDF
  - Track page numbers during extraction
  - Handle extraction errors gracefully

- [x] **T3.2**: Implement text chunking service
  - Use LangChain's RecursiveCharacterTextSplitter
  - Configure: 1000 chars, 200 char overlap
  - Return chunks with metadata (page number, chunk index)

- [x] **T3.3**: Test PDF processing with sample documents
  - Test with multi-page PDF
  - Verify page number tracking
  - Verify chunk count accuracy

---

## Phase 4: Backend Core - Embeddings (FR2.3) ✅

- [x] **T4.1**: Implement OpenAI embeddings service
  - File: `backend/services/embeddings.py`
  - Generate embeddings using text-embedding-3-small
  - Handle OpenAI API errors
  - Return vectors with correct dimensions (1536)

- [x] **T4.2**: Test embedding generation
  - Test with sample text chunks
  - Verify vector dimensions
  - Check API response handling

---

## Phase 5: Backend Core - Upload Endpoint (FR2.4, FR3.1, FR3.4) ✅

- [x] **T5.1**: Create upload router
  - File: `backend/routers/upload.py`
  - POST /api/upload endpoint
  - Accept multipart/form-data (PDF files)
  - Validate file type (.pdf only)

- [x] **T5.2**: Implement complete processing pipeline
  - Extract text from PDF
  - Chunk text
  - Generate embeddings for each chunk
  - Create metadata (filename, page, chunk index, timestamp)
  - Upsert to Pinecone with namespace

- [x] **T5.3**: Return processing results
  - Return JSON with: filename, chunks_created, vectors_stored, namespace
  - Handle and return errors appropriately (400, 422, 503)

- [x] **T5.4**: Create health check endpoint
  - GET /api/health
  - Return Pinecone connection status

---

## Phase 6: Frontend - Upload Interface (FR1.1, FR1.2, FR1.3, FR1.4)

- [ ] **T6.1**: Create file upload component
  - File: `frontend/components/FileUpload.tsx`
  - Drag-and-drop zone (accept .pdf only)
  - Support single and multiple file selection
  - Display selected files before upload

- [ ] **T6.2**: Create status display component
  - File: `frontend/components/StatusDisplay.tsx`
  - Show upload progress
  - Display processing status
  - Show success confirmation with file stats

- [ ] **T6.3**: Build main page
  - File: `frontend/app/page.tsx`
  - Integrate FileUpload component
  - Integrate StatusDisplay component
  - Handle file submission to backend API

- [ ] **T6.4**: Implement upload logic
  - Send files to backend /api/upload
  - Handle response and errors
  - Update UI with processing results

---

## Phase 7: Error Handling & User Feedback (FR4.1, FR4.2, FR4.3)

- [ ] **T7.1**: Add frontend error handling
  - Invalid file type warnings
  - Upload failure messages
  - Processing error display
  - Network error handling

- [ ] **T7.2**: Add backend error responses
  - 400: Invalid file type
  - 422: PDF extraction failure
  - 503: Embedding/Pinecone failures
  - Include helpful error messages

- [ ] **T7.3**: Display processing stats
  - Show chunks created per document
  - Show total vectors stored
  - Show namespace used

---

## Phase 8: Testing & Validation

- [ ] **T8.1**: End-to-end test with sample PDF
  - Upload PDF through frontend
  - Verify vectors in Pinecone dashboard
  - Check metadata is correct

- [ ] **T8.2**: Test error scenarios
  - Upload non-PDF file
  - Upload corrupted PDF
  - Test with very small PDF (1 page)
  - Test with larger PDF (~20 pages)

- [ ] **T8.3**: Verify success criteria
  - Processing time < 30 seconds for typical PDF
  - Support PDFs up to 50MB
  - Clean error messages for failures

---

## Phase 9: Documentation

- [ ] **T9.1**: Create README.md
  - Project description
  - Setup instructions (frontend & backend)
  - Environment variable configuration
  - How to run locally

- [ ] **T9.2**: Add inline code comments where needed
  - Complex logic only
  - Non-obvious architecture decisions

---

## Notes for Future Sessions

- Each task should be completed and tested before moving to the next
- When resuming work, check this file to see current progress
- Mark tasks complete with `[x]` as they're finished
- Add subtasks or notes under tasks as needed during implementation
- Keep the lightweight philosophy: simple, readable code over abstractions

---

## Current Task
**Next up**: T6.1 - Create file upload component

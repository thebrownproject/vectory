# Development Notes

A running diary of development decisions, important context, and session-to-session notes.

---

## Session 1 - October 5, 2025

### Phase 1: Setup & Configuration ✅

**What was completed:**
- Backend FastAPI structure with CORS configured
- Frontend Next.js 15 with TypeScript and Tailwind CSS
- Environment variables configured (templates created)
- All dependencies installed with latest 2025 versions
- VS Code Python interpreter configured

**Important Decisions Made:**

1. **Package Updates:**
   - Replaced `PyPDF2` with `pypdf==6.1.1` (PyPDF2 is deprecated, pypdf is the maintained successor)
   - Replaced `pinecone-client` with `pinecone==7.3.0` (package was renamed in v5.1.0)
   - Using `langchain-text-splitters` only (not full LangChain) to keep dependencies minimal

2. **Version Strategy:**
   - All packages verified against PyPI for latest stable versions as of Oct 2025
   - FastAPI 0.118.0, OpenAI 2.1.0, Pinecone 7.3.0, pypdf 6.1.1, langchain-text-splitters 0.3.11

3. **Git Workflow:**
   - Using branch-per-phase strategy (feature/phase-X-name)
   - Direct merges to main (no PRs for solo development)
   - Commit after each task completion for granular history

4. **Development Environment:**
   - Python virtual environment: `backend/venv/`
   - VS Code settings configured to use venv interpreter
   - Both dev servers running: frontend (port 3000), backend (port 8000)

**FastAPI Auto-Features:**
- Swagger UI available at: `http://localhost:8000/docs`
- ReDoc available at: `http://localhost:8000/redoc`
- No additional configuration needed

**API Keys Status:**
- `.env` files created with placeholders
- ⚠️ **TODO**: Need actual API keys before Phase 3 (Embeddings) and Phase 5 (Upload Endpoint)
  - `OPENAI_API_KEY` - for text-embedding-3-small model
  - `PINECONE_API_KEY` - for vector storage
  - `PINECONE_INDEX_NAME` - create index "vectory" in Pinecone dashboard (1536 dimensions)

**Current Branch:** `feature/phase-2-vector-adapter`

**Next Steps:** Phase 2 - Vector DB Adapter (T2.1, T2.2, T2.3)

---

## Session 2 - October 6, 2025

### Phase 2: Vector DB Adapter ✅

**What was completed:**
- T2.1: Base vector DB adapter interface (`backend/adapters/base_adapter.py`)
- T2.2: Pinecone adapter implementation (`backend/adapters/pinecone_adapter.py`)
- T2.3: Health check endpoint integration and testing

**Important Decisions Made:**

1. **Adapter Pattern Implementation:**
   - Abstract base class `VectorDBAdapter` with two methods: `upsert()` and `health_check()`
   - Type hints for all parameters (vectors, metadata, namespace, ids)
   - Return dictionary from `upsert()` to allow different adapters to return relevant stats
   - Health check returns boolean for simple status checking

2. **Pinecone-Specific Design:**
   - Adapter reads `PINECONE_API_KEY` and `PINECONE_INDEX_NAME` from environment
   - Uses Pinecone SDK v7.3.0 (modern API, no ServerlessSpec import needed for basic operations)
   - Upserts use namespace parameter for document organization
   - Health check uses `describe_index_stats()` to verify connection

3. **Testing Approach:**
   - Health check endpoint at `/api/health` returns Pinecone connection status
   - Created `test_adapter.py` script for manual testing (expects valid API key)
   - Confirmed adapter properly handles missing API keys with clear error messages

**Testing Results:**
- ✅ Health endpoint: `{"status": "ok", "pinecone_connected": true}`
- ✅ Adapter initialization validates environment variables correctly
- ✅ Test upsert successful: 1 vector stored in Pinecone "test" namespace
- ✅ Verified in Pinecone dashboard with correct metadata

**Pinecone Configuration (Final):**
- Index name: `vectory`
- Dimensions: 1536 (for text-embedding-3-small)
- Metric: cosine
- Cloud: AWS / Region: us-east-1
- Plan: Serverless

**Phase Status:** ✅ Complete - Merged to main

**Next Steps:** Phase 3 - PDF Processing (T3.1, T3.2, T3.3)

---

## Session 3 - October 6, 2025

### Phase 3: PDF Processing ✅

**What was completed:**
- T3.1: PDF text extraction service (`backend/services/pdf_processor.py`)
- T3.2: Text chunking implementation with LangChain RecursiveCharacterTextSplitter
- T3.3: Test script created and verified with real PDF

**Important Decisions Made:**

1. **Single-class design for PDF processing:**
   - Combined extraction and chunking in `PDFProcessor` class
   - Two-step process: `extract_text_with_pages()` → `chunk_text()`
   - Convenience method `process_pdf()` for single-call processing
   - Rationale: Extraction and chunking are tightly coupled, always used together

2. **Metadata structure:**
   - Each chunk includes: `page_number`, `chunk_index`, `text`
   - Global `chunk_index` across entire document (not per-page)
   - Empty pages filtered out during extraction
   - This structure maps directly to Pinecone metadata needs

3. **LangChain configuration:**
   - Import: `from langchain_text_splitters import RecursiveCharacterTextSplitter`
   - Chunk size: 1000 characters
   - Overlap: 200 characters
   - Default separators: `["\n\n", "\n", " ", ""]`

4. **Testing approach:**
   - Created `_test_pdf_processor.py` following existing pattern
   - Tested with real 7-page soil report PDF
   - Results: 7 pages → 14 chunks (avg 2 chunks/page)
   - Test only processes to memory, no Pinecone upload

**Testing Results:**
- ✅ Successfully extracted text from 7-page PDF
- ✅ Created 14 chunks with proper metadata
- ✅ Chunk size correctly limited to ~1000 characters
- ✅ Page numbers tracked accurately
- ✅ Combined `process_pdf()` method works end-to-end

**Phase Status:** ✅ Complete - Ready to merge to main

**Current Branch:** `feature/phase-3-pdf-processing`

**Next Steps:** Phase 4 - Embeddings (T4.1, T4.2)

---

## Session 4 - October 6, 2025

### Phase 4: Embeddings ✅

**What was completed:**
- T4.1: OpenAI embeddings service (`backend/services/embeddings.py`)
- T4.2: Test script with comprehensive validation

**Important Decisions Made:**

1. **Context7 Documentation Lookup:**
   - Used Context7 MCP to fetch latest OpenAI Cookbook examples
   - Confirmed modern API pattern: `client.embeddings.create()`
   - Learned batch processing best practices (up to 2048 inputs, cookbook recommends 1000)

2. **Service Implementation:**
   - Class-based `EmbeddingService` with OpenAI client initialization
   - Environment variable validation on instantiation
   - Two methods: `generate_embedding()` for single, `generate_embeddings()` for batch
   - Response parsing: `[item.embedding for item in response.data]`
   - Empty input handling (returns empty list)

3. **API Details:**
   - Model: `text-embedding-3-small`
   - Dimensions: 1536 (verified in tests)
   - Error handling wraps OpenAI exceptions with descriptive messages

**Testing Results:**
- ✅ Single embedding: 1536 dimensions confirmed
- ✅ Batch embeddings: 3 texts → 3 embeddings, all correct dimensions
- ✅ Empty input: Returns empty list without API call
- ✅ All tests use real OpenAI API (not mocked)

**Phase Status:** ✅ Complete - Ready to merge to main

**Current Branch:** `feature/phase-4-embeddings`

**Next Steps:** Phase 5 - Upload Endpoint (T5.1, T5.2, T5.3, T5.4)

---

## Session 5 - October 6, 2025

### Phase 5: Upload Endpoint ✅

**What was completed:**
- T5.1: Upload router with file validation (`backend/routers/upload.py`)
- T5.2: Complete processing pipeline (PDF → chunks → embeddings → Pinecone)
- T5.3: Response handling with comprehensive error codes
- T5.4: Health check endpoint (already existed in main.py)

**Important Decisions Made:**

1. **FastAPI File Upload Pattern:**
   - Used Context7 to fetch latest FastAPI documentation
   - Implemented `List[UploadFile]` for multi-file support
   - Async file reading: `await file.read()`
   - Temporary file handling with proper cleanup

2. **Complete Pipeline Flow:**
   - Save uploaded file to temp location
   - Process PDF → extract & chunk
   - Generate embeddings for all chunks
   - Prepare metadata with timestamp (timezone-aware)
   - Upsert to Pinecone with unique namespace
   - Clean up temp file in `finally` block

3. **Namespace Strategy:**
   - Format: `{filename}-{uuid-8chars}` (e.g., `report.pdf-a1b2c3d4`)
   - Ensures unique namespace per upload
   - Allows same file to be uploaded multiple times

4. **Error Handling:**
   - 400: Invalid file type (non-PDF)
   - 422: PDF extraction failure (no text extracted)
   - 503: Service failures (OpenAI API, Pinecone)
   - HTTPException raised at appropriate points

5. **Metadata Schema (implemented):**
   ```python
   {
     "filename": str,
     "page_number": int,
     "chunk_index": int,
     "upload_timestamp": str (ISO format, UTC),
     "total_chunks": int,
     "text": str
   }
   ```

6. **Datetime Fix:**
   - Fixed deprecation warning: `datetime.utcnow()` → `datetime.now(timezone.utc)`
   - Results in timezone-aware timestamps

**Testing Results:**
- ✅ Server starts successfully with router integrated
- ✅ Health endpoint confirms Pinecone connection
- ✅ Upload endpoint tested via Swagger UI with real PDF
- ✅ PDF successfully chunked and stored in Pinecone
- ✅ All error handling paths defined

**API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Both auto-generated by FastAPI

**Phase Status:** ✅ Complete - Merged to main

**Current Branch:** `feature/phase-5-upload-endpoint` (ready to merge)

**Next Steps:** Phase 6 - Frontend Upload Interface (T6.1, T6.2, T6.3, T6.4)

---

## Session 6 - October 6, 2025

### Code Review & Test Reorganization ✅

**What was completed:**
- Comprehensive code review of all backend code using Context7 documentation
- Fixed type hints in `pdf_processor.py` (`any` → `Any`)
- Added namespace validation in `pinecone_adapter.py`
- Reorganized tests into `backend/tests/` directory following pytest conventions

**Code Review Findings:**

1. **Type Hint Issue (Fixed):**
   - Problem: `any` (built-in function) used instead of `Any` (typing module)
   - Location: `pdf_processor.py` lines 16, 35, 62
   - Fix: Added `from typing import Any` and updated all type hints
   - Impact: Improves type safety for static analysis tools

2. **Namespace Validation (Added):**
   - Problem: No validation preventing empty namespaces
   - Location: `pinecone_adapter.py` upsert method
   - Fix: Added check for non-empty string with clear error message
   - Rationale: Prevents vectors from going into default namespace unexpectedly

3. **Documentation Cross-Check:**
   - ✅ FastAPI usage verified (CORS, file uploads, error handling)
   - ✅ OpenAI client verified (`embeddings.create()` pattern)
   - ✅ Pinecone SDK verified (upsert format, health check method)
   - ✅ PyPDF usage verified (`PdfReader`, `extract_text()`)
   - ✅ LangChain text splitter verified (chunk_size, chunk_overlap parameters)

**Test Reorganization:**

1. **Directory Structure Change:**
   - Before: Test files in `backend/` root with `_test_` prefix
   - After: Test files in `backend/tests/` with `test_` prefix
   - Rationale: Follows Python/pytest best practices

2. **Files Reorganized:**
   - `_test_adapter.py` → `tests/test_adapter.py`
   - `_test_embeddings.py` → `tests/test_embeddings.py`
   - `_test_pdf_processor.py` → `tests/test_pdf_processor.py`
   - `_test_upload_endpoint.py` → `tests/test_upload_endpoint.py`
   - Added `tests/__init__.py` for package structure

3. **Import Fixes:**
   - Added `sys.path.insert(0, str(Path(__file__).parent.parent))` to all test files
   - Allows imports from parent backend directory
   - Verified with successful test run of `test_embeddings.py`

**Testing Results:**
- ✅ `test_embeddings.py` runs successfully with new structure
- ✅ All imports working correctly
- ✅ No code functionality changed, only organization

**Commits Made:**
1. `Fix type hints and add namespace validation` (d10bcd9)
2. `Reorganize tests into tests/ directory` (0555e4a)

**Current Branch:** `main` (fixes applied directly to main)

**Next Steps:**
- Run all tests to verify they work after reorganization
- Update any documentation that references test file locations
- Continue with Phase 6 - Frontend Upload Interface

---

## Session Notes Template (for future sessions)

### Session X - [Date]

**Phase:** [Phase Name]

**What was completed:**
- Task list

**Important Decisions Made:**
- Decision 1
- Decision 2

**Blockers/Issues:**
- Any problems encountered

**Current Branch:** [branch name]

**Next Steps:** [What to tackle next]

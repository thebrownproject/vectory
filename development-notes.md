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

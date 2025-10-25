# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Vectory v2.0 is a multi-user SaaS platform for document knowledge management. Users upload documents (PDF, DOCX, TXT), organize them into "stacks", and search or chat with their content using AI-powered semantic search and RAG.

**Current Status**: v1.0 complete (simple POC). Now building v2.0 (production SaaS platform).

**Portfolio Focus**: v2.0 is designed as a portfolio piece to demonstrate full-stack SaaS development, modern UI design (iOS 26 Liquid Glass), and AI integration skills. Potential for real users/revenue in v3.0.

**Key Features**:
- Multi-user authentication (Supabase Auth)
- Stack-based document organization
- Multi-format document processing (PDF, DOCX, TXT) with Docling
- AI-generated document metadata (titles, descriptions)
- Semantic search across documents
- Liquid Glass UI design (iOS 26 aesthetic)
- Freemium tier with optional Pro chat interface

## Architecture

### Multi-Tier Structure
- **Frontend**: Next.js 15 (App Router) on localhost:3000 - handles auth, document management, search, chat
- **Backend**: FastAPI on localhost:8000 - handles document processing, embeddings, vector search
- **Database**: Supabase (PostgreSQL + Auth + Storage) - user data, document metadata, authentication
- **Vector DB**: ChromaDB (self-hosted) - document embeddings and semantic search

### Processing Pipeline
1. User uploads document → Frontend sends to Supabase Storage → Gets file URL
2. Frontend calls `/api/upload` with file URL and stack_id
3. Backend fetches file from Supabase Storage
4. **Docling** extracts text and structure (supports PDF, DOCX, TXT)
5. **OpenAI GPT-4o-mini** generates title and description from content
6. Backend chunks text using LangChain's RecursiveCharacterTextSplitter (1000 chars, 200 overlap)
7. Backend generates embeddings (OpenAI `text-embedding-3-small`, 1536 dimensions)
8. Backend upserts to **ChromaDB** collection for that stack
9. Backend updates Supabase document record with metadata and status
10. Frontend displays AI-generated title/description

### Multi-Tenant Architecture
- **Row-Level Security (RLS)**: Supabase enforces data isolation at database level
- **Stack Collections**: Each user stack gets a unique ChromaDB collection (`stack_{stack_id}`)
- **Freemium Limits**: Backend validates tier limits (1 stack, 5 docs, 50MB for free tier)

### Vector DB Adapter Pattern (Maintained from v1.0)
The backend continues to use the adapter pattern for vector database abstraction:

- **Base class**: `backend/adapters/base_adapter.py` - defines `upsert()`, `search()`, `health_check()`
- **v2.0 implementation**: `backend/adapters/chroma_adapter.py`
- **v1.0 implementation**: `backend/adapters/pinecone_adapter.py` (still available for compatibility)
- **Future implementations**: Weaviate, Qdrant (swap via `VECTOR_DB_PROVIDER` env var)

This allows switching vector databases with minimal code changes.

## Development Commands

### ChromaDB (Vector Database)
```bash
# Run ChromaDB in Docker (required before starting backend)
docker run -d -p 8001:8000 --name chromadb -v chromadb_data:/chroma/chroma chromadb/chroma:latest

# Or use Docker Compose (recommended)
docker-compose up -d chromadb
```

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

### Full Stack Startup (Recommended)
```bash
# Terminal 1: Start ChromaDB
docker-compose up chromadb

# Terminal 2: Start backend
cd backend && source venv/bin/activate && uvicorn main:app --reload --port 8000

# Terminal 3: Start frontend
cd frontend && npm run dev
```

## Environment Configuration

### Backend `.env`
```
# OpenAI (embeddings + metadata generation)
OPENAI_API_KEY=sk-...

# Supabase (auth + database + storage)
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJhbG...
SUPABASE_SERVICE_KEY=eyJhbG...  # For server-side operations

# ChromaDB (vector database)
CHROMA_HOST=localhost
CHROMA_PORT=8001
VECTOR_DB_PROVIDER=chroma  # For adapter switching

# v1.0 Compatibility (if using Pinecone adapter)
# PINECONE_API_KEY=...
# PINECONE_INDEX_NAME=vectory
# VECTOR_DB_PROVIDER=pinecone
```

### Frontend `.env.local`
```
# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000

# Supabase (public keys safe for frontend)
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbG...
```

## API Contract

### Authentication Endpoints
- **POST /api/auth/signup** - Create new user account (email + password)
- **POST /api/auth/login** - Login user (returns JWT)
- **POST /api/auth/logout** - Logout user
- **GET /api/auth/user** - Get current user info

### Stack Endpoints
- **GET /api/stacks** - List all user's stacks
- **POST /api/stacks** - Create new stack (freemium: max 1 for free tier)
  - Input: `{"name": "My Documents", "description": "..."}`
  - Output: `{"id": "uuid", "name": "...", "created_at": "..."}`
- **DELETE /api/stacks/{stack_id}** - Delete stack and all documents

### Document Endpoints
- **POST /api/upload** - Upload document to stack
  - Input: `{"file_url": "supabase-storage-url", "stack_id": "uuid"}`
  - Output: `{"document_id": "uuid", "title": "AI-generated", "description": "AI summary", "status": "processing"}`
  - Errors: 400 (invalid file), 413 (exceeds 50MB), 403 (freemium limit exceeded), 503 (processing failure)

- **GET /api/stacks/{stack_id}/documents** - List all documents in stack
- **GET /api/documents/{document_id}** - Get document details + metadata
- **DELETE /api/documents/{document_id}** - Delete document

### Search Endpoints
- **POST /api/search** - Semantic search within stack
  - Input: `{"query": "search text", "stack_id": "uuid", "limit": 10}`
  - Output: `{"results": [{"text": "...", "document_id": "...", "relevance_score": 0.89}]}`

### Chat Endpoints (Pro Tier - Phase 8)
- **POST /api/chat** - Chat with documents (RAG)
  - Input: `{"message": "...", "stack_id": "uuid", "conversation_id": "uuid"}`
  - Output: `{"response": "AI answer", "sources": [{"document_id": "...", "text": "..."}]}`

### Health Endpoint
- **GET /api/health** - Check service status
  - Output: `{"status": "ok", "chroma_connected": true, "supabase_connected": true}`

## Metadata Schema

### Supabase Documents Table
Each document record in PostgreSQL includes:
```json
{
  "id": "uuid",
  "stack_id": "uuid",
  "filename": "document.pdf",
  "file_url": "https://supabase.co/storage/...",
  "file_size": 2048576,
  "title": "Q4 Financial Report",  // AI-generated
  "description": "Summary of quarterly financial performance...",  // AI-generated
  "status": "completed",  // uploaded, processing, completed, failed
  "uploaded_at": "2025-10-25T14:30:00Z",
  "processed_at": "2025-10-25T14:30:27Z"
}
```

### ChromaDB Vector Metadata
Each vector in ChromaDB includes:
```json
{
  "document_id": "uuid",
  "filename": "document.pdf",
  "page_number": 3,
  "chunk_index": 12,
  "total_chunks": 45,
  "section": "Introduction",  // from Docling structure
  "text": "original chunk text..."
}
```

## Code Philosophy

**v2.0 is portfolio-first. Balance functionality with polish and clarity.**

### Core Principles
- **Clean, readable code**: Prioritize clarity over cleverness
- **Modern patterns**: Use TypeScript discriminated unions, React hooks, proper separation of concerns
- **Type safety**: Leverage TypeScript and Pydantic for compile-time guarantees
- **Small functions**: Keep functions under 50 lines, single responsibility
- **Comment strategically**: Explain "why" for complex decisions, not "what" for obvious code
- **Test thoughtfully**: Focus on user flows and critical paths, not 100% coverage

### Portfolio Considerations
- **Visual polish matters**: Liquid Glass UI demonstrates modern design skills
- **Demo-ability**: Build features that look impressive in videos/screenshots
- **Document decisions**: Architecture Decision Records (ADRs) show strategic thinking
- **Clean git history**: Granular commits demonstrate professional development workflow

### Intentional Complexity
v2.0 adds complexity where it provides value:
- **Adapter pattern**: Maintains v1.0 pattern for vector DB abstraction
- **RLS policies**: Database-level security is worth the learning curve
- **Liquid Glass**: Complex CSS/animations demonstrate UI engineering skills
- **Multi-tenancy**: Shows understanding of SaaS architecture patterns

### Avoid
- Over-engineering with unnecessary microservices or complex state management
- Premature optimization (profile first, optimize later)
- "Just in case" features not in the PRD
- Adding libraries for trivial tasks native code can handle

## Task Tracking

**Always check `docs/v2.0/tasks-v2.0.md` when starting work.** It contains the complete v2.0 development roadmap broken into 10 phases over 12 weeks. Mark tasks complete with `[x]` as you finish them.

**Reference documentation in `docs/v2.0/`:**
- `tasks-v2.0.md` - Complete task breakdown with acceptance criteria
- `ARCHITECTURE-v2.0.md` - Architecture Decision Records (ADRs) and design rationale
- `prd-v2.0.md` - Product requirements and user stories
- `frontend-design-guide-v2.0.md` - Liquid Glass design system and UI patterns

**v1.0 reference materials in `docs/v1.0/`:**
- Available for reference but v1.0 is complete
- Adapter pattern from v1.0 is maintained in v2.0

**v2.0 development sequence (12 weeks):**
1. **Foundation & Supabase Setup** (Weeks 1-2) - Auth, database, RLS
2. **Multi-User Architecture** (Weeks 2-3) - Stacks, freemium limits
3. **ChromaDB Integration** (Weeks 3-4) - Vector storage, collections
4. **Docling Integration** (Weeks 4-5) - Multi-format processing, AI metadata
5. **Document Management UI** (Weeks 5-6) - Upload, list, detail views
6. **Search Interface** (Weeks 6-7) - Semantic search UI and backend
7. **Liquid Glass UI Polish** (Weeks 7-9) - Design system, animations, responsive
8. **Chat Interface [Optional]** (Weeks 9-10) - RAG with ChatKit (Pro tier)
9. **Testing & Validation** (Week 10) - E2E, multi-user, performance
10. **Documentation & Deployment** (Weeks 11-12) - README, deploy, demo

## Key Constraints

### Performance Targets
- **Document processing**: <30 seconds from upload to searchable (typical document)
- **Search response time**: <1 second for semantic search queries (95th percentile)
- **UI performance**: 60fps for Liquid Glass animations on modern devices

### File Support
- **Formats**: PDF, DOCX, TXT only
- **File size limit**: 50MB per file
- **No OCR**: Scanned/image-based PDFs will have poor extraction quality

### Freemium Limits (Enforced server-side)
- **Free Tier**: 1 stack, 5 documents per stack, 50MB total storage, no chat
- **Pro Tier**: Unlimited stacks/documents, chat interface (payment in v3.0)

### Infrastructure
- **Development**: Local (Docker Compose for ChromaDB)
- **Production**: Railway/Fly.io + Supabase Cloud (deployment in Phase 10)
- **ChromaDB**: Self-hosted (not managed service)

### AI Models
- **Embeddings**: OpenAI `text-embedding-3-small` (1536 dimensions)
- **Metadata generation**: OpenAI `gpt-4o-mini`
- **Chat (Pro tier)**: OpenAI `gpt-4o` or `gpt-4o-mini`

## In Scope (v2.0)

✅ Multi-user authentication (Supabase Auth)
✅ Stack-based document organization
✅ Multi-format document processing (PDF, DOCX, TXT via Docling)
✅ AI-generated metadata (titles, descriptions)
✅ Semantic search across documents
✅ Liquid Glass UI design (iOS 26 aesthetic)
✅ Freemium tier enforcement
✅ Deployment (Railway/Fly.io)
✅ Chat interface with RAG (Pro tier - Phase 8, optional)

## Out of Scope (Deferred to v3.0)

❌ Payment processing (Stripe integration)
❌ Collaborative stacks (team sharing)
❌ Document versioning
❌ Advanced analytics/dashboards
❌ OCR for scanned documents
❌ MCP server for developer access (mentioned in PRD but deferred)
❌ Custom embedding models (local models)
❌ Batch document upload
❌ Public API for integrations

## Git Workflow

**Repository**: https://github.com/thebrownproject/vectory

**Branch Structure**:
- `main` - v1.0 stable release (complete, functional POC)
- `v2.0-dev` - v2.0 development branch (created from main)
- Feature branches off `v2.0-dev` for major phases (optional)

**Branching Strategy for v2.0**:

### Option 1: Single v2.0-dev Branch (Recommended for solo development)
```bash
git checkout main
git checkout -b v2.0-dev
# Work directly on v2.0-dev, committing after each task
# Merge to main when v2.0 is complete and tested
```

### Option 2: Phase-Based Feature Branches (For larger phases)
```bash
git checkout v2.0-dev
git checkout -b feature/v2-phase-1-foundation
# Complete Phase 1 tasks
# Merge back to v2.0-dev when phase complete
```

**Development Workflow**:
1. Check `docs/v2.0/tasks-v2.0.md` to identify current task
2. Complete a single task (e.g., T1.1)
3. Test task completion
4. Commit immediately with task reference:
   ```bash
   git add .
   git commit -m "Complete T1.1: Set up Supabase project

   - Created Supabase project in cloud dashboard
   - Configured project settings and region
   - Added environment variables to .env
   - Tested connection from local development"
   ```
5. Move to next task
6. Repeat steps 2-5 until phase complete
7. Push regularly: `git push origin v2.0-dev`

**Important Practices**:
- ✅ Commit after EACH task completion (granular history)
- ✅ Include task ID in commit message (e.g., "Complete T1.1:")
- ✅ Test before committing
- ✅ Push at end of each development session
- ✅ Write descriptive commit messages (explain what AND why)
- ❌ Don't batch multiple tasks into one commit
- ❌ Don't commit broken code

**Commit Message Format**:
```
Complete T[X.Y]: [Brief description in imperative mood]

- Bullet point: specific change made
- Bullet point: another change made
- Reference related tasks if applicable (e.g., "Part of Phase 1 foundation")
```

**Example Good Commits**:
```
Complete T1.3: Create database schema in Supabase

- Created profiles, stacks, documents tables
- Added foreign key relationships
- Set up proper indexes for query performance
- Documented schema in ARCHITECTURE-v2.0.md
```

```
Complete T7.2: Build Liquid Glass top bar component

- Created TopBar.tsx with glassmorphic styling
- Implemented scroll-based height/opacity changes
- Added Framer Motion animations for smooth transitions
- Tested responsive behavior on mobile/desktop
```

**Merging v2.0 to Main**:
When v2.0 is complete, tested, and ready for release:
```bash
git checkout main
git merge v2.0-dev --no-ff  # Creates merge commit for clear history
git tag v2.0.0
git push origin main --tags
```

**Keeping v1.0 Accessible**:
v1.0 remains on `main` branch history. Create tag for reference:
```bash
git checkout main
git tag v1.0.0 [commit-hash-of-last-v1-commit]
git push origin v1.0.0
```

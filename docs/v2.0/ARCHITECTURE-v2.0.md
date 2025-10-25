# Vectory v2.0 - Architecture Decisions

This file documents key architectural and design decisions made during v2.0 development (October 2025 onwards).

For v1.0 architecture decisions, see `docs/v1.0/ARCHITECTURE-v1.0.md`.

---

## ADR-001: Supabase for Authentication and Database

**Date:** 2025-10-25
**Status:** Planned
**Context:** v2.0 requires multi-user authentication, user data storage, and file storage. Need to choose between building custom auth + database or using a Backend-as-a-Service (BaaS).

**Decision:** Use Supabase for authentication, PostgreSQL database, and file storage.

**Alternatives Considered:**
- **Custom FastAPI auth + PostgreSQL** - Rejected: Time-consuming to build securely, need to implement JWT handling, password hashing, email verification
- **Firebase** - Rejected: Vendor lock-in, pricing less predictable at scale, less control over data
- **Auth0 + separate database** - Rejected: More complex to integrate, additional service to manage
- **Clerk + Neon** - Considered: Good developer experience, but Supabase offers more integrated features

**Consequences:**
- ✅ Built-in authentication with email verification, OAuth ready for future
- ✅ Row-Level Security (RLS) provides database-level multi-tenancy isolation
- ✅ Storage buckets for file management with built-in access control
- ✅ Real-time subscriptions available for future features
- ✅ Free tier sufficient for development and early users
- ✅ Can self-host Supabase later if needed (open-source)
- ❌ Adds external dependency (though open-source mitigates risk)
- ❌ Learning curve for Supabase-specific patterns

**References:**
- Implementation: Phase 1 tasks (T1.1-T1.5)
- Database schema: See "Database Schema" section below

---

## ADR-002: ChromaDB for Vector Storage (Replacing Pinecone)

**Date:** 2025-10-25
**Status:** Planned
**Context:** v1.0 uses Pinecone (hosted, paid vector database). For v2.0 SaaS, need to choose vector database that supports multi-tenant architecture at reasonable cost.

**Decision:** Self-host ChromaDB for vector storage, with per-stack collections.

**Alternatives Considered:**
- **Continue with Pinecone** - Rejected: Cost scales with number of vectors (expensive for SaaS), less control over infrastructure
- **Weaviate** - Considered: Powerful but complex, heavier resource requirements
- **Qdrant** - Considered: Excellent performance, but ChromaDB has simpler Python API
- **Milvus** - Rejected: Enterprise-focused, overkill for MVP needs

**Consequences:**
- ✅ Full control over vector database infrastructure
- ✅ No per-vector pricing (fixed hosting cost regardless of scale)
- ✅ Simple Python API, easy to integrate with LangChain
- ✅ Per-stack collections provide natural multi-tenant isolation
- ✅ Can persist to disk for durability
- ✅ Supports metadata filtering for advanced queries
- ❌ Need to manage hosting and backups ourselves
- ❌ Not as mature as Pinecone (less battle-tested at scale)
- ❌ Requires Docker/infrastructure setup

**Implementation Strategy:**
- Development: Run ChromaDB in local Docker container
- Production: Deploy alongside FastAPI in same Docker Compose stack
- Collections: One ChromaDB collection per user stack (`stack_{stack_id}`)
- Persistence: Mount volume for ChromaDB data directory

**References:**
- Implementation: Phase 3 tasks (T3.1-T3.5)
- Adapter pattern maintained from v1.0 for future database swaps

---

## ADR-003: Docling for Document Processing (Replacing pypdf)

**Date:** 2025-10-25
**Status:** Planned
**Context:** v1.0 uses pypdf for PDF text extraction. v2.0 needs to support multiple formats (PDF, DOCX, TXT) and extract structured information beyond raw text.

**Decision:** Use Docling for document processing and text extraction.

**Alternatives Considered:**
- **Continue with pypdf** - Rejected: PDF-only, basic text extraction, no layout understanding
- **PyPDF2 + python-docx + custom logic** - Rejected: Fragmented approach, each library has different API
- **Apache Tika** - Considered: Mature, many formats, but requires Java runtime
- **Unstructured.io** - Considered: Excellent but newer, Docling more focused on our use case
- **LlamaIndex document loaders** - Considered: Good abstraction but adds heavy dependency

**Consequences:**
- ✅ Single library handles PDF, DOCX, TXT (unified API)
- ✅ Preserves document structure (headings, tables, lists)
- ✅ Better chunking context (can split by sections/headings)
- ✅ Layout-aware extraction (better quality than raw text)
- ✅ Active development and maintenance
- ❌ Additional dependency with its own sub-dependencies
- ❌ May have higher memory/CPU requirements than simple pypdf
- ❌ Newer library (less community resources than pypdf)

**Integration Points:**
- Replaces `backend/services/pdf_processor.py` with `backend/services/docling_processor.py`
- Returns structured text suitable for intelligent chunking
- Feeds into AI metadata generation (title/description)

**References:**
- Implementation: Phase 4 tasks (T4.1-T4.5)
- Testing: Validate with PDF, DOCX, TXT files

---

## ADR-004: AI-Generated Document Metadata

**Date:** 2025-10-25
**Status:** Planned
**Context:** Users shouldn't need to manually title and describe documents. System should automatically generate meaningful metadata from document content.

**Decision:** Use OpenAI GPT-4o-mini to generate document titles and descriptions automatically during upload.

**Alternatives Considered:**
- **Manual user input** - Rejected: Poor UX, friction during upload
- **Filename only** - Rejected: Filenames often uninformative ("Document1.pdf")
- **Extract first heading** - Rejected: Doesn't work for all document types, may not be meaningful
- **Use Claude API** - Considered: Similar capability, but OpenAI already used for embeddings
- **Local LLM (Llama)** - Rejected: Adds infrastructure complexity, slower than API call

**Consequences:**
- ✅ Zero manual effort from users
- ✅ Consistent, meaningful metadata across all documents
- ✅ Improves document discovery and organization
- ✅ Creates better UX than manual input
- ❌ Additional API cost per document upload (~$0.0001 per document with GPT-4o-mini)
- ❌ Adds latency to processing pipeline (~2-3s)
- ❌ Quality depends on document content (garbage in, garbage out)

**Implementation Details:**
- Service: `backend/services/metadata_generator.py`
- Model: `gpt-4o-mini` (fast, cheap, sufficient for summarization)
- Prompt: Extract 1-2 sentence summary and generate concise title
- Fallback: If AI fails, use filename as title
- Store: Title and description in Supabase `documents` table

**References:**
- Implementation: Phase 4 (T4.3)
- User story: US-3 (automated metadata generation)

---

## ADR-005: Stack-Based Document Organization

**Date:** 2025-10-25
**Status:** Planned
**Context:** Users need to organize documents by project, client, or topic. Flat "all documents" list doesn't scale.

**Decision:** Implement "Stacks" as the primary organizational unit - collections of related documents.

**Alternatives Considered:**
- **Folders/hierarchies** - Rejected: Complex to implement, harder UX (where to put things)
- **Tags only** - Rejected: Too flexible, users struggle with tagging discipline
- **Single document list** - Rejected: Doesn't scale beyond ~20 documents
- **Projects + subprojects** - Rejected: Over-engineered for v2.0 scope

**Consequences:**
- ✅ Simple mental model: "Stack = collection of documents on one topic"
- ✅ Natural isolation boundary (each stack has own ChromaDB collection)
- ✅ Easy to implement search within stack
- ✅ Freemium limits easy to enforce (1 stack for free, unlimited for Pro)
- ✅ Future: can add sharing/collaboration at stack level
- ❌ No hierarchy (can't nest stacks)
- ❌ Documents can't belong to multiple stacks without duplication

**Implementation:**
- Database: `stacks` table with `user_id` foreign key
- Each document belongs to exactly one stack
- UI: Stack selector in top bar for quick switching
- ChromaDB: One collection per stack (`stack_{id}`)

**References:**
- Implementation: Phase 2 (T2.4-T2.5)
- User story: US-1 (create and organize by stack)

---

## ADR-006: Row-Level Security for Multi-Tenancy

**Date:** 2025-10-25
**Status:** Planned
**Context:** Multi-user SaaS requires complete data isolation between users. Need to prevent users from accessing each other's data.

**Decision:** Use Supabase Row-Level Security (RLS) policies for database-level access control.

**Alternatives Considered:**
- **Application-level filtering** (WHERE user_id = current_user) - Rejected: Prone to bugs, can forget in queries
- **Separate databases per user** - Rejected: Doesn't scale, complex to manage
- **Schema-based isolation** (one schema per user) - Rejected: PostgreSQL limit on schemas, complex migrations
- **Custom middleware** - Rejected: Reinventing the wheel, less secure than database-level

**Consequences:**
- ✅ Database enforces isolation automatically (can't forget in queries)
- ✅ Protection against SQL injection and authorization bugs
- ✅ Policies defined once, applied everywhere
- ✅ Supabase client handles auth context automatically
- ✅ Easier to audit security (review policies vs all queries)
- ❌ PostgreSQL RLS has performance overhead (mitigated by proper indexes)
- ❌ Debugging RLS errors can be tricky initially

**RLS Policy Examples:**

```sql
-- Users can only read their own stacks
CREATE POLICY "Users can view own stacks"
  ON stacks FOR SELECT
  USING (auth.uid() = user_id);

-- Users can only insert stacks for themselves
CREATE POLICY "Users can create own stacks"
  ON stacks FOR INSERT
  WITH CHECK (auth.uid() = user_id);
```

**References:**
- Implementation: Phase 1 (T1.4)
- All tables: `profiles`, `stacks`, `documents`, `conversations`, `messages`

---

## ADR-007: Freemium Tier Enforcement

**Date:** 2025-10-25
**Status:** Planned
**Context:** v2.0 is portfolio-first with eventual monetization. Need freemium limits that encourage conversion without complex billing initially.

**Decision:** Enforce limits server-side with clear errors, no payment integration in v2.0.

**Limits:**
- **Free Tier**: 1 stack, 5 documents per stack, 50MB total storage, no chat
- **Pro Tier**: Unlimited stacks/documents, chat interface (payment in v3.0)

**Alternatives Considered:**
- **No limits in v2.0** - Rejected: Doesn't demonstrate SaaS thinking for portfolio
- **Hard-coded tier in database** - Rejected: Not flexible for testing
- **Stripe integration now** - Rejected: Out of scope for 12-week timeline
- **Usage-based limits (API calls)** - Rejected: Too complex to track/enforce

**Consequences:**
- ✅ Demonstrates freemium SaaS concept for portfolio
- ✅ Can manually upgrade test users to Pro for testing
- ✅ Clear upgrade path for v3.0 (add Stripe, remove manual tier assignment)
- ✅ Limits are reasonable for testing (5 docs enough to demo search)
- ❌ No automated payment/upgrade in v2.0
- ❌ Tier stored in `profiles` table (manual assignment initially)

**Enforcement Points:**
- Backend validation in upload endpoint (check stack count, doc count, storage)
- Chat endpoint checks tier before allowing access
- Clear error messages: "Free tier allows 1 stack. Upgrade to create more."

**References:**
- Implementation: Phase 2 (T2.6)
- Future: Phase 8 optional tasks mention Pro tier gating

---

## ADR-008: Liquid Glass Design System

**Date:** 2025-10-25
**Status:** Planned
**Context:** v2.0 aims for portfolio-quality polish. Need to choose design aesthetic that demonstrates modern UI skills.

**Decision:** Implement iOS 26 Liquid Glass design language using Framer Motion and custom CSS.

**Alternatives Considered:**
- **Material Design** - Rejected: Overused, doesn't stand out
- **Tailwind default styling** - Rejected: Too generic for portfolio
- **Brutalist design** - Considered: Trendy but may not age well
- **Traditional glassmorphism** - Rejected: 2021 trend, Liquid Glass is evolution
- **shadcn/ui default theme** - Rejected: Good foundation but needs customization

**Consequences:**
- ✅ Modern, cutting-edge design (iOS 26 launched Sept 2025)
- ✅ Demonstrates awareness of design trends
- ✅ Visually distinctive for portfolio demos
- ✅ Framer Motion animations add professional polish
- ✅ Shows ability to implement complex CSS effects
- ❌ `backdrop-filter` is computationally expensive (need performance testing)
- ❌ Accessibility concerns (iOS 26 criticized for low contrast)
- ❌ Not supported in very old browsers (fallback needed)

**Implementation Strategy:**
- Phase 7 dedicated to Liquid Glass polish (after core functionality works)
- Start with "Tinted" mode (better contrast than full transparency)
- Test performance on mobile devices
- Provide fallback for browsers without `backdrop-filter` support
- Use Framer Motion for physics-based animations

**Design Tokens:**
```css
--glass-bg: rgba(255, 255, 255, 0.08);
--glass-blur: blur(20px) saturate(180%);
--spring-stiffness: 300;
--spring-damping: 24;
```

**References:**
- Implementation: Phase 7 tasks (T7.1-T7.9)
- Design guide: `frontend-design-guide-v2.0.md` Section 11

---

## ADR-009: No Sidebar Navigation (Top Bar Only)

**Date:** 2025-10-25
**Status:** Planned
**Context:** Need to decide primary navigation pattern. Traditional SaaS apps use left sidebar, but iOS 26 focuses on content-first design.

**Decision:** Use fixed top bar for all navigation, no sidebar.

**Alternatives Considered:**
- **Left sidebar** - Rejected: Takes horizontal space, feels desktop-centric
- **Bottom tab bar (mobile pattern)** - Rejected: Inconsistent with desktop experience
- **Hamburger menu** - Rejected: Hidden navigation reduces discoverability
- **Top bar + sidebar combo** - Rejected: Too much chrome, content not primary

**Consequences:**
- ✅ Maximizes content area (no sidebar taking 200-300px)
- ✅ Works seamlessly on mobile (no sidebar collapse/drawer needed)
- ✅ Aligns with iOS 26 content-first philosophy
- ✅ Simpler implementation (one navigation component)
- ✅ Liquid Glass top bar becomes hero element
- ❌ Limited space for navigation items (need to prioritize)
- ❌ May need dropdown menus for secondary actions

**Top Bar Layout:**
```
┌────────────────────────────────────────────┐
│ Logo  Stack▾   Search🔍  Chat💬  User👤   │
└────────────────────────────────────────────┘
```

**Mobile Adaptation:**
- Logo remains (small)
- Stack selector becomes dropdown
- Search/Chat become icon-only
- User menu in hamburger on smallest screens

**References:**
- Implementation: Phase 7 (T7.2 - Build Liquid Glass top bar)
- Design guide: Section 4 (Layout & Components)

---

## ADR-010: Synchronous Processing (No Background Jobs)

**Date:** 2025-10-25
**Status:** Planned
**Context:** Document processing includes: upload → Docling extraction → AI metadata → chunking → embedding → ChromaDB storage. Need to decide if this happens synchronously or in background.

**Decision:** Keep processing synchronous for v2.0 (process during upload request).

**Alternatives Considered:**
- **Celery + Redis** - Rejected: Adds infrastructure complexity, overkill for MVP
- **FastAPI BackgroundTasks** - Considered: Simple, but no retry logic or failure handling
- **Cloud functions** (AWS Lambda) - Rejected: Need persistent ChromaDB connection
- **Polling with status updates** - Rejected: More complex frontend, websockets needed

**Consequences:**
- ✅ Simpler architecture (no job queue, no workers)
- ✅ Easier to debug (everything happens in one request)
- ✅ User gets immediate feedback (success or error)
- ✅ No additional infrastructure (Redis, Celery, etc.)
- ❌ Upload endpoint has longer response time (~20-30s)
- ❌ Risk of timeout with very large files (mitigated by 50MB limit)
- ❌ No retry logic if processing fails midway

**Mitigations:**
- Set request timeout to 60s (enough for 50MB processing)
- Show real-time progress updates to user (status messages)
- Keep processing optimized (target <30s for typical document)
- If scalability issues in v3.0, can refactor to background jobs

**References:**
- Implementation: Phase 4 (T4.4 - Update upload endpoint)
- Success criteria: Processing time <30s

---

## Technical Stack Summary

### **Frontend**
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript 5
- **Styling**: Tailwind CSS 4 + Custom Liquid Glass CSS
- **UI Components**: shadcn/ui (customized)
- **Animations**: Framer Motion
- **Chat UI**: OpenAI ChatKit (Phase 8 - optional)
- **Auth Client**: @supabase/auth-helpers-nextjs
- **State**: React hooks + Context API (no Redux needed for v2.0)

### **Backend**
- **Framework**: FastAPI (Python 3.11+)
- **Document Processing**: Docling (multi-format extraction)
- **Text Chunking**: LangChain text-splitters
- **Embeddings**: OpenAI text-embedding-3-small (1536 dimensions)
- **LLM**: OpenAI GPT-4o-mini (for metadata generation, chat)
- **Vector DB**: ChromaDB (self-hosted)
- **Database Client**: Supabase Python client
- **File Handling**: python-multipart

### **Data Layer**
- **Auth**: Supabase Auth (email, future OAuth)
- **Database**: Supabase PostgreSQL
- **File Storage**: Supabase Storage (buckets)
- **Vector Storage**: ChromaDB (Docker container)
- **Caching**: None initially (can add Redis in v3.0 if needed)

### **Infrastructure**
- **Development**: Docker Compose (FastAPI + ChromaDB)
- **Deployment**: Railway / Fly.io / VPS
- **Monitoring**: Vercel Analytics (frontend), basic logging (backend)
- **Error Tracking**: Optional - Sentry

### **API Integration**
- **OpenAI**: Embeddings + Chat Completion
- **Supabase**: Auth, Database, Storage

---

## Database Schema

### **Supabase PostgreSQL Tables**

#### **profiles**
Extends Supabase auth.users with app-specific data
```sql
CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id),
  email TEXT NOT NULL,
  tier TEXT DEFAULT 'free', -- 'free' or 'pro'
  storage_used_bytes BIGINT DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS: Users can only view/update their own profile
```

#### **stacks**
Document collections
```sql
CREATE TABLE stacks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS: Users can only access their own stacks
CREATE INDEX idx_stacks_user_id ON stacks(user_id);
```

#### **documents**
Document metadata (one row per uploaded file)
```sql
CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  stack_id UUID NOT NULL REFERENCES stacks(id) ON DELETE CASCADE,
  filename TEXT NOT NULL,
  file_url TEXT NOT NULL, -- Supabase Storage URL
  file_size BIGINT NOT NULL,
  title TEXT, -- AI-generated
  description TEXT, -- AI-generated
  status TEXT DEFAULT 'uploaded', -- uploaded, processing, completed, failed
  error_message TEXT,
  uploaded_at TIMESTAMPTZ DEFAULT NOW(),
  processed_at TIMESTAMPTZ
);

-- RLS: Users can only access documents in their stacks (via stack_id)
CREATE INDEX idx_documents_stack_id ON documents(stack_id);
CREATE INDEX idx_documents_status ON documents(status);
```

#### **conversations** (Phase 8 - Optional)
Chat conversation history
```sql
CREATE TABLE conversations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  stack_id UUID NOT NULL REFERENCES stacks(id) ON DELETE CASCADE,
  title TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_conversations_stack_id ON conversations(stack_id);
```

#### **messages** (Phase 8 - Optional)
Individual chat messages
```sql
CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  role TEXT NOT NULL, -- 'user' or 'assistant'
  content TEXT NOT NULL,
  sources JSONB, -- Referenced document chunks
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
```

### **ChromaDB Collections**

Each stack has a ChromaDB collection:
- **Collection naming**: `stack_{stack_id}`
- **Metadata per vector**:
  ```json
  {
    "document_id": "uuid",
    "filename": "document.pdf",
    "chunk_index": 12,
    "total_chunks": 45,
    "page_number": 3,
    "section": "Introduction",
    "text": "original chunk text..."
  }
  ```

---

## Data Flow Diagrams

### **Upload & Processing Flow**

```
1. User uploads file
   ↓
2. Frontend → Supabase Storage (save file, get URL)
   ↓
3. Frontend → POST /api/upload (file URL, stack_id)
   ↓
4. Backend:
   a. Docling extracts text
   b. GPT-4o-mini generates title/description
   c. LangChain chunks text
   d. OpenAI generates embeddings
   e. ChromaDB stores vectors
   f. Supabase updates document record (status: completed)
   ↓
5. Frontend shows success + AI metadata
```

### **Search Flow**

```
1. User enters search query
   ↓
2. Frontend → POST /api/search (query, stack_id)
   ↓
3. Backend:
   a. OpenAI generates query embedding
   b. ChromaDB searches collection for top-N matches
   c. Returns results with metadata
   ↓
4. Frontend displays passages with source links
```

### **Chat Flow (Phase 8 - Optional)**

```
1. User sends message
   ↓
2. Frontend → POST /api/chat (message, stack_id, conversation_id?)
   ↓
3. Backend:
   a. OpenAI generates message embedding
   b. ChromaDB searches for relevant chunks
   c. Constructs prompt: system + retrieved chunks + user message
   d. OpenAI generates chat response
   e. Saves message + response to Supabase
   ↓
4. Frontend displays AI response with source citations
```

---

## Security Considerations

### **Authentication**
- Supabase handles password hashing (bcrypt)
- JWT tokens for session management
- Email verification required for signup
- Rate limiting on auth endpoints (Supabase built-in)

### **Authorization**
- Row-Level Security enforces user data isolation
- All Supabase queries include auth context automatically
- ChromaDB collections scoped per stack (backend validates user owns stack)

### **File Upload**
- File type validation: only PDF, DOCX, TXT allowed
- File size limit: 50MB per file
- Storage bucket policies: users can only upload to their own paths
- Virus scanning: Not implemented in v2.0 (consider for v3.0)

### **API Security**
- CORS configured for frontend domain only
- API keys stored in environment variables
- No API keys exposed to frontend
- Rate limiting: Consider adding in production (e.g., 100 req/min per user)

### **Data Privacy**
- Documents stored in Supabase (encrypted at rest)
- Vectors in ChromaDB (consider encryption for production)
- OpenAI API: Data not used for training (opt-out enabled)
- No analytics tracking beyond basic Vercel Analytics

---

## Performance Targets

### **Processing**
- Document upload → searchable: **<30 seconds** (50th percentile)
- Target 95th percentile: <60 seconds
- Bottlenecks: Docling extraction (~5-10s), embedding generation (~3-5s per batch)

### **Search**
- Query → results: **<1 second** (95th percentile)
- Target: <500ms for typical queries
- Optimization: ChromaDB HNSW index, limit results to top-10

### **UI Performance**
- Liquid Glass effects: **60fps** on modern devices
- Consider reducing effects on mobile if <30fps
- Lazy load document lists (virtualization if >100 docs)

### **API Limits**
- OpenAI embeddings: 3000 requests/min (sufficient for MVP)
- Supabase free tier: 500MB database, 1GB storage (monitor usage)
- ChromaDB: Memory-dependent (1GB RAM = ~1M vectors @ 1536 dims)

---

## Deployment Architecture

### **Development**
```
Localhost:
- Frontend: Next.js dev server (localhost:3000)
- Backend: FastAPI uvicorn (localhost:8000)
- ChromaDB: Docker container (localhost:8001)
- Supabase: Cloud (remote)
```

### **Production (Planned)**
```
Frontend (Vercel):
- Next.js deployed to Vercel
- Edge Functions for SSR
- Environment variables for Supabase URL

Backend (Railway/Fly.io):
- Docker Compose with:
  - FastAPI container
  - ChromaDB container
- Persistent volume for ChromaDB data
- Environment variables for API keys

Supabase:
- Cloud-hosted (free tier → paid as needed)
- Or self-hosted if cost becomes issue
```

---

## Migration from v1.0

### **What Stays the Same**
- ✅ Adapter pattern for vector databases (base_adapter.py)
- ✅ LangChain text splitters (same chunking logic)
- ✅ OpenAI embeddings (text-embedding-3-small, 1536 dims)
- ✅ FastAPI backend framework
- ✅ Next.js frontend framework

### **What Changes**
- ❌ ~~Pinecone~~ → ChromaDB (new adapter implementation)
- ❌ ~~pypdf~~ → Docling (new processor)
- ❌ Single-user → Multi-user (Supabase Auth)
- ❌ Local files → Supabase Storage
- ❌ No database → Supabase PostgreSQL
- ❌ Simple UI → Liquid Glass design system

### **Migration Strategy**
v1.0 remains on `main` branch as working reference. v2.0 built on `v2.0-dev` branch with incremental changes. No automated data migration needed (v1.0 and v2.0 are separate systems).

---

## Future Architecture Considerations (v3.0 and Beyond)

### **Scalability Improvements**
1. **Background Job Processing**
   - Add Celery + Redis for async document processing
   - Allows handling large batches and retry logic

2. **Caching Layer**
   - Redis cache for frequent searches
   - Cache AI-generated metadata

3. **Database Optimization**
   - PostgreSQL read replicas for search queries
   - Partition large tables by user_id

### **Advanced Features**
1. **Collaborative Stacks**
   - Share stacks with team members
   - Permission levels (view, edit, admin)

2. **Advanced Search**
   - Hybrid search (semantic + keyword)
   - Filters (date, document type, source)

3. **Custom Embedding Models**
   - Option to use local models (lower cost, privacy)
   - Support for domain-specific embeddings

### **Monetization**
1. **Payment Integration**
   - Stripe for subscription billing
   - Usage-based pricing tiers

2. **Enterprise Features**
   - SSO (SAML)
   - Audit logs
   - Data export

3. **API Access**
   - Public API for integrations
   - API key management

### **Infrastructure**
1. **Kubernetes Deployment**
   - Replace Docker Compose with K8s for scaling
   - Auto-scaling based on load

2. **Monitoring & Observability**
   - OpenTelemetry tracing
   - Prometheus metrics
   - Grafana dashboards

---

## Open Questions & Decisions Deferred

### **To Be Decided During Development**
1. **ChromaDB persistence strategy**: Disk vs in-memory + periodic snapshots?
2. **Search ranking algorithm**: Pure cosine similarity or add recency/popularity signals?
3. **Chat token limits**: Max conversation length before truncation?
4. **Dark mode default**: Auto-detect system preference or default to light?
5. **Mobile-first or desktop-first**: Which to optimize first?

### **Out of Scope for v2.0**
- Document versioning
- Collaboration features
- Advanced analytics
- Custom branding
- Webhook integrations
- API for third-party integrations
- OCR for scanned documents
- Multi-language support

---

This architecture document will be updated as implementation progresses and decisions are refined.

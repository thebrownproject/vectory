# Development Notes - v2.0

A running diary of development decisions, important context, and session-to-session notes for Vectory v2.0.

**Note:** v1.0 development notes are in `docs/v1.0/development-notes-v1.0.md`

---

## Session 1 - October 25, 2025

### Phase 0: Planning & Documentation ✅

**What was completed:**
- Created comprehensive v2.0 Product Requirements Document (PRD)
- Created Frontend Design Guide with iOS 26 Liquid Glass specifications
- Created Architecture Decision Records (10 ADRs documenting all major technical decisions)
- Created detailed task breakdown (86 tasks across 10 phases, 12-week timeline)
- Updated CLAUDE.md with v2.0 project context
- Researched iOS 26 Liquid Glass design language for modern UI direction

**Important Decisions Made:**

1. **Strategic Direction:**
   - **v2.0 Scope**: Portfolio-first SaaS platform with potential for real users/revenue in v3.0
   - **Timeline**: 12 weeks standard (all features including optional chat)
   - **Focus**: Demonstrate full-stack SaaS skills, modern UI design, and AI integration
   - **Differentiation**: iOS 26 Liquid Glass aesthetic (cutting-edge design trend from Sept 2025)

2. **Technical Stack Evolution (v1.0 → v2.0):**

   **What Changes:**
   - ❌ ~~Pinecone (hosted, paid)~~ → ✅ ChromaDB (self-hosted, open-source)
   - ❌ ~~pypdf (basic extraction)~~ → ✅ Docling (multi-format, structure-aware)
   - ❌ ~~Single-user, local storage~~ → ✅ Multi-tenant with Supabase (Auth + DB + Storage)
   - ❌ ~~PDF only~~ → ✅ PDF, DOCX, TXT support
   - ❌ ~~Simple UI~~ → ✅ Liquid Glass design system with Framer Motion
   - ❌ ~~No metadata~~ → ✅ AI-generated titles/descriptions (GPT-4o-mini)

   **What Stays:**
   - ✅ Adapter pattern for vector databases (base_adapter.py maintained)
   - ✅ FastAPI backend + Next.js 15 frontend
   - ✅ OpenAI text-embedding-3-small (1536 dimensions)
   - ✅ LangChain text splitters (1000 chars, 200 overlap)
   - ✅ Clean code philosophy

3. **Architecture Decision Records (ADRs):**

   **ADR-001: Supabase for Auth & Database**
   - Chose Supabase over Firebase, Auth0, or custom auth
   - Rationale: Integrated auth/DB/storage, open-source (can self-host), RLS for security
   - Trade-off: External dependency, but open-source mitigates vendor lock-in

   **ADR-002: ChromaDB for Vector Storage**
   - Chose self-hosted ChromaDB over Pinecone (hosted)
   - Rationale: Cost scales better for SaaS (fixed hosting vs per-vector pricing), full control
   - Trade-off: More infrastructure complexity, but Docker simplifies deployment

   **ADR-003: Docling for Document Processing**
   - Chose Docling over pypdf + python-docx + custom parsers
   - Rationale: Single library handles multiple formats, preserves document structure
   - Trade-off: Newer library (less community resources), but solves core use case well

   **ADR-004: AI-Generated Document Metadata**
   - Use GPT-4o-mini to auto-generate titles and descriptions on upload
   - Rationale: Zero manual effort from users, improves UX, creates better search
   - Trade-off: ~$0.0001 per document + 2-3s latency, but worth it for UX

   **ADR-005: Stack-Based Document Organization**
   - Documents organized into "stacks" (collections) vs flat list or folders
   - Rationale: Simple mental model, natural isolation boundary, maps to ChromaDB collections
   - Trade-off: No hierarchy, but avoids over-complexity for v2.0

   **ADR-006: Row-Level Security for Multi-Tenancy**
   - Use Supabase RLS policies instead of application-level filtering
   - Rationale: Database enforces isolation automatically, prevents auth bugs
   - Trade-off: Performance overhead (mitigated by indexes), but security first

   **ADR-007: Freemium Tier Enforcement**
   - Server-side limits: Free (1 stack, 5 docs, 50MB) vs Pro (unlimited + chat)
   - Rationale: Demonstrates SaaS thinking without building payment in v2.0
   - Trade-off: Manual tier assignment initially, Stripe integration deferred to v3.0

   **ADR-008: Liquid Glass Design System**
   - iOS 26 Liquid Glass aesthetic vs Material Design or traditional glassmorphism
   - Rationale: Cutting-edge (Sept 2025 release), portfolio standout, shows design awareness
   - Trade-off: Computationally expensive (backdrop-filter), requires performance testing

   **ADR-009: No Sidebar Navigation (Top Bar Only)**
   - Fixed top bar for all navigation vs sidebar pattern
   - Rationale: Maximizes content area, works seamlessly on mobile, aligns with iOS 26
   - Trade-off: Limited space for nav items, but dropdown menus solve this

   **ADR-010: Synchronous Processing (No Background Jobs)**
   - Process documents during upload request (no Celery/Redis queue)
   - Rationale: Simpler architecture for MVP, immediate user feedback
   - Trade-off: Longer request time (~30s), but acceptable with 50MB limit + progress UI

4. **Design System Research:**
   - **iOS 26 Liquid Glass**: Announced WWDC 2025 (June 9), released iOS 26 (Sept 15, 2025)
   - **Key characteristics**: Translucent meta-material, physically accurate lensing, real-time specular highlights
   - **Design lineage**: Mac OS X Aqua → iOS 7 blurs → iPhone X gestures → Dynamic Island → visionOS → Liquid Glass
   - **Reception**: Polarizing (some love dynamic aesthetic, others criticize accessibility/contrast)
   - **Implementation approach**: Start with "Tinted" mode (more opaque, better contrast) per iOS 26.1 update
   - **Tools**: Framer Motion for physics-based animations, custom CSS for glassmorphic effects

5. **Development Sequence (10 Phases over 12 Weeks):**
   - **Phase 1** (Weeks 1-2): Foundation & Supabase Setup
   - **Phase 2** (Weeks 2-3): Multi-User Architecture (stacks, freemium)
   - **Phase 3** (Weeks 3-4): ChromaDB Integration
   - **Phase 4** (Weeks 4-5): Docling Integration + AI Metadata
   - **Phase 5** (Weeks 5-6): Document Management UI
   - **Phase 6** (Weeks 6-7): Search Interface
   - **Phase 7** (Weeks 7-9): Liquid Glass UI Polish
   - **Phase 8** (Weeks 9-10): Chat Interface [Optional - Pro Tier]
   - **Phase 9** (Week 10): Testing & Validation
   - **Phase 10** (Weeks 11-12): Documentation & Deployment

6. **Git Strategy for v2.0:**
   - Create `v2.0-dev` branch from `main`
   - Commit after each task completion (granular history)
   - Optional: phase-based feature branches for major phases
   - Merge to `main` when v2.0 complete and tested
   - Tag releases: `v1.0.0` (existing), `v2.0.0` (future)

**Documentation Created:**

1. **`docs/v2.0/prd-v2.0.md`** (Product Requirements)
   - User stories (6 core user stories)
   - Functional requirements (core features, tech stack, success metrics)
   - 12-week roadmap (MVP → Pro release)
   - Target users: Developers, professionals, researchers, early adopters

2. **`docs/v2.0/frontend-design-guide-v2.0.md`** (Design System)
   - Original sections: glassmorphism, Framer Motion, component guide
   - **Section 11 added**: iOS 26 Liquid Glass design direction
   - CSS patterns (base glass, tinted mode for accessibility)
   - Framer Motion integration examples
   - Performance considerations and fallbacks
   - Color palette (light/dark modes)
   - Implementation priority (phased approach)

3. **`docs/v2.0/ARCHITECTURE-v2.0.md`** (Architecture Decisions)
   - 10 Architecture Decision Records (ADRs)
   - Technical stack summary (frontend, backend, data layer, infrastructure)
   - Database schema (5 tables: profiles, stacks, documents, conversations, messages)
   - ChromaDB collection structure and metadata format
   - Data flow diagrams (upload, search, chat)
   - Security considerations (auth, authorization, file upload, API)
   - Performance targets (processing <30s, search <1s, UI 60fps)
   - Deployment architecture (dev vs production)
   - Migration strategy from v1.0
   - Future considerations for v3.0

4. **`docs/v2.0/tasks-v2.0.md`** (Implementation Roadmap)
   - 86 tasks across 10 phases
   - Each task includes:
     - Clear description
     - Acceptance criteria
     - File locations (where code will live)
     - Testing expectations
   - Structured like v1.0 tasks (same clarity and thoroughness)
   - Success criteria at bottom (what "done" looks like)

5. **`CLAUDE.md`** (Updated for v2.0)
   - Project overview updated (v1.0 → v2.0 transition)
   - Architecture section updated (multi-tier with Supabase + ChromaDB)
   - Processing pipeline updated (10 steps with Docling + AI metadata)
   - Development commands updated (added ChromaDB Docker setup)
   - Environment variables updated (Supabase keys added)
   - API contract updated (15+ endpoints documented)
   - Metadata schema updated (dual: Supabase tables + ChromaDB vectors)
   - Code philosophy updated (portfolio-first, intentional complexity)
   - Task tracking updated (points to v2.0 docs)
   - Constraints updated (performance targets, freemium limits)
   - Scope updated (in-scope vs out-of-scope for v2.0)
   - Git workflow updated (v2.0-dev branch strategy)

**Key Insights from Research:**

1. **Liquid Glass Design Language:**
   - Biggest iOS visual change since iOS 7 (2013)
   - Unified across all Apple platforms (iOS, iPadOS, macOS, watchOS, tvOS)
   - "Translucent meta-material that reflects and refracts surroundings"
   - Real-time rendering with specular highlights
   - Controversial: some users complain about low contrast, Apple added "Tinted" mode in iOS 26.1
   - Nielsen Norman Group critique: "Liquid Glass Is Cracked, and Usability Suffers"
   - **Our approach**: Start with tinted mode (better contrast), test performance early

2. **ChromaDB vs Pinecone Cost Analysis:**
   - Pinecone: ~$70/month for 100K vectors (scales per vector)
   - ChromaDB: Fixed hosting cost ($20-40/month VPS) regardless of vector count
   - At 1M vectors: Pinecone ~$500/month, ChromaDB same $20-40/month
   - Trade-off: More infrastructure management, but massive cost savings at scale

3. **Docling Capabilities:**
   - Supports PDF, DOCX, PPTX, images, HTML, Markdown, AsciiDoc, Excel
   - Preserves document structure (headings, tables, lists, layout)
   - OCR support via Tesseract integration
   - Layout analysis for better chunking
   - Actively developed by IBM Research
   - Python-native, integrates well with LangChain

**Scope Clarifications:**

**IN SCOPE for v2.0:**
- ✅ Multi-user authentication
- ✅ Stack-based organization
- ✅ PDF/DOCX/TXT processing
- ✅ AI metadata generation
- ✅ Semantic search
- ✅ Liquid Glass UI
- ✅ Freemium enforcement
- ✅ Deployment
- ✅ Chat with RAG (Pro tier - Phase 8, optional)

**OUT OF SCOPE (Deferred to v3.0):**
- ❌ Payment processing (Stripe)
- ❌ Collaborative stacks
- ❌ Document versioning
- ❌ Advanced analytics
- ❌ OCR for scanned PDFs
- ❌ MCP server for developers
- ❌ Custom embedding models
- ❌ Batch upload
- ❌ Public API

**Technical Constraints Agreed Upon:**

**Performance Targets:**
- Document processing: <30 seconds upload → searchable
- Search response: <1 second (95th percentile)
- UI animations: 60fps on modern devices

**File Support:**
- Formats: PDF, DOCX, TXT only (no images, no OCR initially)
- Size limit: 50MB per file
- Scanned PDFs: Poor quality expected (no OCR in v2.0)

**Freemium Limits:**
- Free tier: 1 stack, 5 documents, 50MB total storage, no chat
- Pro tier: Unlimited stacks/docs, chat interface (payment in v3.0)

**Infrastructure:**
- Development: Local (Docker Compose for ChromaDB)
- Production: Railway or Fly.io + Supabase Cloud
- ChromaDB: Self-hosted (not managed service)

**Current Status:**

- ✅ All planning documentation complete
- ✅ Technical decisions documented and rationalized
- ✅ Design direction researched and specified
- ✅ Tasks broken down into actionable items
- ✅ Git strategy defined
- 🎯 Ready to begin Phase 1 development

**Current Branch:** `main` (planning docs committed)

**Next Steps:**

**Immediate (Next Session):**
1. Create `v2.0-dev` branch from `main`
2. Begin Phase 1, Task 1.1: Set up Supabase project
   - Create Supabase account + new project
   - Configure project settings and region
   - Add environment variables to `backend/.env`
   - Test connection from local development

**Week 1-2 Goals:**
- Complete entire Phase 1 (Foundation & Supabase Setup)
- Tasks T1.1 through T1.6
- Deliverable: Working Supabase integration with auth, database schema, RLS, and storage

**Success Criteria for This Session:**
- ✅ Comprehensive planning documentation created
- ✅ All major technical decisions documented with rationale
- ✅ Design direction researched and specified
- ✅ Clear 12-week roadmap established
- ✅ CLAUDE.md updated for v2.0 context

---

## Session Notes Template (for future sessions)

### Session X - [Date]

**Phase:** [Phase Name and Number]

**What was completed:**
- Task list with IDs (e.g., T1.1, T1.2)

**Important Decisions Made:**
- Decision 1 with rationale
- Decision 2 with trade-offs

**Technical Discoveries:**
- Learnings about libraries, APIs, or patterns

**Blockers/Issues:**
- Any problems encountered and how resolved

**Testing Results:**
- What was tested and outcomes

**Current Branch:** [branch name]

**Next Steps:** [What to tackle next session]

---

## Notes for Future Sessions

- **Always check `tasks-v2.0.md`** before starting work to identify current task
- **Reference ADRs in `ARCHITECTURE-v2.0.md`** when making technical decisions
- **Follow design guide** in `frontend-design-guide-v2.0.md` for UI implementation
- **Commit after each task** with format: `Complete T[X.Y]: [description]`
- **Update this file** at end of each session with decisions and progress
- **Test before committing** - no broken code in history

---

## v2.0 Development Principles

**Portfolio Focus:**
- Prioritize visual polish and demo-ability
- Document architectural decisions in ADRs
- Maintain clean git history with granular commits
- Build features that look impressive in videos/screenshots

**Code Quality:**
- Write clean, readable code (clarity over cleverness)
- Use modern patterns (TypeScript discriminated unions, React hooks)
- Leverage type safety (TypeScript + Pydantic)
- Keep functions small (<50 lines, single responsibility)
- Comment strategically (explain "why", not "what")

**Intentional Complexity:**
- Adapter pattern: Maintained from v1.0 for vector DB abstraction
- RLS policies: Database-level security worth the learning curve
- Liquid Glass: Complex CSS/animations demonstrate UI skills
- Multi-tenancy: Shows SaaS architecture understanding

**Avoid:**
- Over-engineering (no unnecessary microservices or complex state management)
- Premature optimization (profile first, optimize later)
- "Just in case" features (stick to PRD scope)
- Adding libraries for trivial tasks (native code often sufficient)

---

**Project Status:** 🎯 Planning Complete - Ready for Development
**Timeline:** 12 weeks (Oct 25, 2025 - Jan 16, 2026)
**Next Milestone:** Phase 1 Complete (Supabase foundation) - Target: Nov 8, 2025

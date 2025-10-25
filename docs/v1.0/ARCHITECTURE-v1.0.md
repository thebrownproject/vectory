# Vectory v1.0 - Architecture Decisions

This file documents key architectural and design decisions made during v1.0 development (October 2025).

For detailed session-by-session notes, see `development-notes-v1.0.md`.

---

## ADR-001: Adapter Pattern for Vector Database Portability

**Date:** 2025-10-06
**Status:** Implemented
**Context:** Need to support multiple vector databases (Pinecone, Chroma, Supabase, Weaviate) without refactoring application code.

**Decision:** Implement abstract base class `VectorDBAdapter` with two core methods:
- `upsert(vectors, metadata, namespace, ids)` - Store vectors
- `health_check()` - Verify connection

Concrete implementations in `backend/adapters/` directory.

**Alternatives Considered:**
- Duck typing (no formal interface) - Rejected: No type safety, easy to break contracts
- Single Pinecone implementation - Rejected: Vendor lock-in, hard to migrate later
- Factory pattern with config - Considered but overkill for this POC

**Consequences:**
- ✅ Can swap vector DB via `VECTOR_DB_PROVIDER` environment variable
- ✅ Easy to add new adapters (implement 2 methods)
- ✅ Type-safe contracts enforced by abstract class
- ❌ Slight complexity increase (abstract base class + inheritance)

**References:**
- Implementation: `backend/adapters/base_adapter.py`, `backend/adapters/pinecone_adapter.py`
- Discussion: development-notes-v1.0.md (Session 2)

---

## ADR-002: Controlled Component Pattern for FileUpload

**Date:** 2025-10-08
**Status:** Implemented
**Context:** FileUpload component initially had internal `selectedFiles` state. Parent component also had `files` state. Two sources of truth caused sync bugs where removing a file didn't update the upload button correctly.

**Decision:** Refactor FileUpload to controlled component pattern:
- Parent (`page.tsx`) manages `files` state (single source of truth)
- FileUpload receives `files` prop and `onFilesChange` callback
- FileUpload has no internal file state

**Alternatives Considered:**
- Uncontrolled component with refs - Rejected: Imperative API, harder to test
- Context API - Rejected: Overkill for parent-child relationship
- Keep duplicate state with sync logic - Rejected: Bug-prone, violates DRY

**Consequences:**
- ✅ Single source of truth eliminates sync bugs
- ✅ Easier to test (pass different props to FileUpload)
- ✅ Parent controls entire upload lifecycle
- ❌ More props passing (slight verbosity)

**References:**
- Implementation: `frontend/components/FileUpload.tsx`, `frontend/app/page.tsx`
- Discussion: development-notes-v1.0.md (Session 8)

---

## ADR-003: Discriminated Unions for Type-Safe State Management

**Date:** 2025-10-08
**Status:** Implemented
**Context:** Upload status needed to track multiple states (idle, uploading, success, error) with different data for each state. Traditional approach would use multiple boolean flags, which allows impossible states.

**Decision:** Use TypeScript discriminated unions for `UploadStatus` type:
```typescript
type UploadStatus =
  | { state: "idle" }
  | { state: "uploading"; filesCount: number }
  | { state: "success"; results: UploadResult[] }
  | { state: "error"; message: string };
```

**Alternatives Considered:**
- Multiple booleans (isLoading, isError, isSuccess) - Rejected: Allows impossible states like `isError && isSuccess`
- Single string + separate data fields - Rejected: No type safety on which fields are valid
- State machine library (XState) - Rejected: Overkill for simple state transitions

**Consequences:**
- ✅ TypeScript enforces exhaustive checking in StatusDisplay
- ✅ Impossible states can't exist at compile time
- ✅ Clear type inference (e.g., `status.state === "success"` narrows to success type)
- ❌ Requires understanding of discriminated unions (learning curve)

**References:**
- Implementation: `frontend/components/StatusDisplay.tsx`
- TypeScript docs: Discriminated Unions
- Discussion: development-notes-v1.0.md (Session 8)

---

## ADR-004: Service Layer for API Communication

**Date:** 2025-10-08
**Status:** Implemented
**Context:** Upload logic initially inline in `page.tsx`. As complexity grew (FormData creation, error handling, response parsing), component became cluttered.

**Decision:** Extract API logic to service layer in `frontend/lib/api.ts`:
- Pure functions (no React dependencies)
- Single responsibility: handle HTTP communication
- Type-safe interfaces for requests/responses
- Export reusable functions like `uploadPDFs()`

**Alternatives Considered:**
- Keep logic in component - Rejected: Violates separation of concerns
- Custom React hooks (useUpload) - Considered: Would add value but not needed for POC
- API client library (axios, ky) - Rejected: Native fetch is sufficient for simple POST

**Consequences:**
- ✅ Component stays focused on UI/state management
- ✅ API logic is easily testable (no React needed)
- ✅ Reusable across multiple components if needed
- ❌ Extra file to maintain (slight overhead)

**References:**
- Implementation: `frontend/lib/api.ts`
- Discussion: development-notes-v1.0.md (Session 8)

---

## ADR-005: Namespace Strategy for Vector Isolation

**Date:** 2025-10-06
**Status:** Implemented
**Context:** Need to isolate vectors by upload session to allow querying specific documents and support re-uploading the same file.

**Decision:** Use namespace format `{filename}-{uuid-8chars}` for each upload:
- Example: `report.pdf-a1b2c3d4`
- Generated in `upload.py` using `uuid.uuid4().hex[:8]`
- Stored with each vector in Pinecone

**Alternatives Considered:**
- Timestamp-based: `report.pdf-20251006143000` - Rejected: Harder to debug, timezone confusion
- Sequential counter: `report.pdf-1`, `report.pdf-2` - Rejected: Requires state tracking
- Filename only (no UUID) - Rejected: Can't re-upload same file

**Consequences:**
- ✅ Each upload is uniquely identifiable
- ✅ Same file can be uploaded multiple times without conflicts
- ✅ Easy to query vectors by namespace
- ❌ Can't easily identify "latest" version of a document (requires timestamp metadata)

**References:**
- Implementation: `backend/routers/upload.py` (line 70)
- Discussion: development-notes-v1.0.md (Session 5)

---

## Technical Stack Summary

**Frontend:**
- Next.js 15 (App Router) - React framework with SSR capabilities
- TypeScript 5 - Type safety and modern JavaScript features
- Tailwind CSS 4 - Utility-first styling
- react-dropzone - Drag-and-drop file upload handling

**Backend:**
- FastAPI 0.118 - High-performance Python web framework
- pypdf 6.1.1 - PDF text extraction (replaces deprecated PyPDF2)
- LangChain text-splitters 0.3.11 - Intelligent text chunking
- OpenAI 2.1.0 - Embedding generation (text-embedding-3-small)
- Pinecone 7.3.0 - Vector database storage

**Development:**
- Git with granular commits (commit per task)
- Branch-per-phase strategy
- VS Code/Cursor for development

---

## Future Architecture Considerations

**For v2.0 and beyond:**

1. **Authentication Layer:**
   - Current: No authentication (local development only)
   - Consider: JWT tokens, user namespaces, role-based access

2. **Multi-Format Support:**
   - Current: PDF only
   - Consider: Abstract `DocumentProcessor` interface for Word/Excel/Images

3. **Query Interface:**
   - Current: Vectors queryable via Claude Desktop MCP only
   - Consider: Built-in semantic search UI with Pinecone query API

4. **Batch Processing:**
   - Current: Synchronous upload (blocking)
   - Consider: Background jobs with Celery/RQ for large files

5. **Monitoring:**
   - Current: Basic health check endpoint
   - Consider: OpenTelemetry tracing, Sentry error tracking

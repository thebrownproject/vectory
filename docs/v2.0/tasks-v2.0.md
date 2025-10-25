# Vectory v2.0 - Development Tasks

**Timeline:** 12 weeks (standard, all features)
**Focus:** Portfolio-first with potential for real users/revenue in v3.0
**Design:** iOS 26 Liquid Glass aesthetic

---

## Project Status: Planning Phase 🎯
**Branch:** `v2.0-dev` (to be created from `main`)

---

## Phase 1: Foundation & Supabase Setup (Weeks 1-2)

### **T1.1**: Set up Supabase project
- Create new Supabase project (Cloud free tier for MVP)
- Configure project settings and region
- Save project URL and anon key to environment variables
- Test connection from local development

### **T1.2**: Configure Supabase Auth
- Enable email authentication in Supabase dashboard
- Configure email templates for signup/verification
- Set up auth policies and redirect URLs
- Test email signup flow manually

### **T1.3**: Create database schema in Supabase Postgres
**Tables to create:**
- `profiles` - User profile information
  - id (uuid, references auth.users)
  - email, created_at, updated_at
- `stacks` - Document collections
  - id, user_id, name, description, created_at
- `documents` - Document metadata
  - id, stack_id, filename, file_url, file_size, status, uploaded_at, processed_at
  - title (AI-generated), description (AI-generated)
- `processing_status` - Track document processing state
  - document_id, status (uploaded, extracting, embedding, completed, failed), error_message

### **T1.4**: Implement Row-Level Security (RLS)
- Enable RLS on all tables
- Create policies: users can only read/write their own data
- Test RLS with multiple test accounts
- Verify data isolation between users

### **T1.5**: Set up Supabase Storage
- Create storage bucket for document files
- Configure bucket policies (private, user-specific access)
- Set file size limits (50MB max per file)
- Test file upload and retrieval

### **T1.6**: Update environment variables
- Add Supabase keys to `backend/.env`
- Add Supabase URL to `frontend/.env.local`
- Update `.env.example` files with new variables
- Document all required environment variables

---

## Phase 2: Multi-User Architecture (Weeks 2-3)

### **T2.1**: Add Supabase client to frontend
- Install `@supabase/supabase-js` and `@supabase/auth-helpers-nextjs`
- Create Supabase client configuration
- Set up auth context/provider for user state management
- Create utility functions for auth operations

### **T2.2**: Build authentication UI
- Create login page (`/login`)
- Create signup page (`/signup`)
- Create password reset flow
- Add email verification handling
- Style with basic Tailwind (Liquid Glass polish comes later)

### **T2.3**: Implement protected routes
- Create auth middleware for Next.js App Router
- Redirect unauthenticated users to login
- Redirect authenticated users away from login/signup
- Test route protection

### **T2.4**: Create "Stacks" concept in backend
- File: `backend/services/stack_service.py`
- Functions: create_stack, get_user_stacks, delete_stack
- Integrate with Supabase client
- Handle errors and validation

### **T2.5**: Build Stacks UI
- Create stacks list page (`/stacks`)
- Add "Create New Stack" button and modal
- Display user's existing stacks
- Allow stack selection (sets active stack for uploads)
- Basic styling with Tailwind

### **T2.6**: Implement freemium limits
- Backend validation: max 1 stack for free tier
- Backend validation: max 5 documents per stack for free tier
- Backend validation: max 50MB total storage for free tier
- Return clear error messages when limits exceeded
- Store tier information in user profile

---

## Phase 3: ChromaDB Integration (Weeks 3-4)

### **T3.1**: Set up self-hosted ChromaDB
- Install ChromaDB in backend environment
- Configure ChromaDB for local development
- Create initialization script for ChromaDB server
- Document ChromaDB setup instructions

### **T3.2**: Update vector DB adapter for ChromaDB
- File: `backend/adapters/chroma_adapter.py`
- Inherit from existing `base_adapter.py`
- Implement `upsert()` method for ChromaDB
- Implement `health_check()` method
- Implement `search()` method for semantic search

### **T3.3**: Create per-stack collections in ChromaDB
- Each stack gets unique ChromaDB collection ID
- Collection naming convention: `stack_{stack_id}`
- Auto-create collection on first document upload to stack
- Handle collection deletion when stack is deleted

### **T3.4**: Update environment configuration
- Add `VECTOR_DB_PROVIDER=chroma` to backend `.env`
- Update adapter factory to load ChromaDB adapter
- Test adapter switching (verify Pinecone still works for v1.0 compatibility)

### **T3.5**: Migrate embedding pipeline to ChromaDB
- Update upload endpoint to use ChromaDB adapter
- Modify metadata structure for ChromaDB format
- Test end-to-end: upload → embed → store in ChromaDB
- Verify vectors are stored in correct collection

---

## Phase 4: Docling Integration (Weeks 4-5)

### **T4.1**: Install and configure Docling
- Add Docling to `requirements.txt`
- Install Docling dependencies
- Test Docling with sample PDF, DOCX, TXT files
- Verify Docling output format

### **T4.2**: Create Docling extraction service
- File: `backend/services/docling_processor.py`
- Replace `pdf_processor.py` functionality
- Extract text from PDF, DOCX, TXT formats
- Preserve document structure (headings, paragraphs, lists)
- Return structured text with metadata

### **T4.3**: Implement AI-powered title/description generation
- File: `backend/services/metadata_generator.py`
- Use OpenAI GPT-4o-mini for summarization
- Generate document title from first page/section
- Generate 1-2 sentence description
- Return confidence scores

### **T4.4**: Update upload endpoint for Docling
- File: `backend/routers/upload.py`
- Replace pypdf calls with Docling processor
- Add AI metadata generation step
- Store title/description in Supabase documents table
- Update processing status tracking

### **T4.5**: Test multi-format document processing
- Test with PDF documents (digital and scanned)
- Test with DOCX files
- Test with TXT files
- Verify title/description quality
- Measure processing time (target: <30s)

---

## Phase 5: Document Management UI (Weeks 5-6)

### **T5.1**: Build document list component
- File: `frontend/components/DocumentList.tsx`
- Display all documents in active stack
- Show: title, description, filename, upload date, status
- Support sorting (by date, name)
- Support filtering (by status)

### **T5.2**: Create document upload flow
- Update FileUpload component for multi-format support
- Accept: PDF, DOCX, TXT files
- Show real-time upload progress
- Display processing status updates
  - "Uploading..." → "Extracting text..." → "Generating summary..." → "Embedding..." → "Complete"
- Clear success/error notifications

### **T5.3**: Add document detail view
- Create document detail page (`/stacks/[stackId]/documents/[documentId]`)
- Display full metadata (title, description, filename, size, dates)
- Show AI-generated summary
- Show processing status and any errors
- Add "Delete Document" action

### **T5.4**: Implement document deletion
- Backend endpoint: DELETE `/api/documents/{id}`
- Delete file from Supabase Storage
- Delete vectors from ChromaDB collection
- Delete metadata from Supabase Postgres
- Update document count and storage usage

### **T5.5**: Add stack switcher to UI
- Create stack selector component (dropdown in top bar)
- Display all user stacks
- Allow switching between stacks
- Update document list when stack changes
- Show current stack name prominently

---

## Phase 6: Search Interface (Weeks 6-7)

### **T6.1**: Implement semantic search backend
- File: `backend/routers/search.py`
- POST `/api/search` endpoint
- Accept query text and stack_id
- Generate query embedding using OpenAI
- Search ChromaDB collection for top-N results
- Return results with source metadata and relevance scores

### **T6.2**: Build search UI component
- File: `frontend/components/SearchBar.tsx`
- Search input with icon (top bar)
- Real-time search as user types (debounced)
- Loading state while searching

### **T6.3**: Create search results display
- File: `frontend/components/SearchResults.tsx`
- Display relevant passages with highlighting
- Show source document name and page/section
- Show relevance score
- Click result to jump to document detail

### **T6.4**: Add search page
- Create search page (`/stacks/[stackId]/search`)
- Full-page search interface
- Recent searches history (client-side)
- Clear search and filters
- Empty state with helpful prompts

### **T6.5**: Test search accuracy
- Test with various query types (questions, keywords, phrases)
- Verify results are relevant
- Measure response time (target: <1s)
- Test with edge cases (empty stack, no results)

---

## Phase 7: Liquid Glass UI Polish (Weeks 7-9)

### **T7.1**: Set up design system
- Install Framer Motion: `npm install framer-motion`
- Create CSS variables for Liquid Glass colors (see design guide)
- Create base glass components using shadcn/ui
- Set up Tailwind config with custom glassmorphic utilities

### **T7.2**: Build Liquid Glass top bar
- File: `frontend/components/TopBar.tsx`
- Fixed position, full width, glassmorphic background
- Layout: Logo (left) | Stack Selector (center) | Search, User Menu (right)
- Implement scroll-based behavior:
  - Default: 64px height, tinted transparency
  - On scroll down: Shrink to 56px, increase transparency
  - On scroll up: Expand back to 64px
- Add Framer Motion animations for smooth transitions

### **T7.3**: Apply Liquid Glass to document cards
- Update DocumentList to use card components
- Glassmorphic background with backdrop blur
- Subtle hover animations (scale 1.0 → 1.02)
- Specular highlights on hover
- Rounded corners, soft shadows

### **T7.4**: Polish upload interface
- Update FileUpload component with Liquid Glass styling
- Animated dropzone with gradient border
- Progress indicators with liquid animations
- Success/error states with smooth transitions
- Icon animations using Framer Motion

### **T7.5**: Add loading states and skeletons
- Create Skeleton component with glassmorphic style
- Use during data loading (document list, search results)
- Animated shimmer effect
- Smooth transition from skeleton to real content

### **T7.6**: Implement modals and overlays
- Create Modal component with Liquid Glass background
- Use for: stack creation, document deletion confirmations, settings
- AnimatePresence for enter/exit animations
- Backdrop blur on overlay

### **T7.7**: Polish micro-interactions
- Button hover states (scale, glow)
- Input focus animations (border glow)
- Icon transitions (spin, bounce)
- Page transitions using Framer Motion page variants
- Smooth scrolling behavior

### **T7.8**: Test responsive design
- Test on mobile (320px - 768px)
- Test on tablet (768px - 1024px)
- Test on desktop (1024px+)
- Adjust glass effects for mobile performance
- Ensure touch targets are adequate (44px minimum)

### **T7.9**: Dark mode support
- Implement dark mode toggle in user menu
- Update CSS variables for dark mode colors
- Adjust glass opacity for dark backgrounds
- Test all components in both modes
- Persist user preference in local storage

---

## Phase 8: Chat Interface [Pro Tier - Optional] (Weeks 9-10)

### **T8.1**: Install OpenAI ChatKit
- Add ChatKit dependencies to frontend
- Configure ChatKit with project settings
- Create chat page (`/stacks/[stackId]/chat`)

### **T8.2**: Build RAG pipeline backend
- File: `backend/routers/chat.py`
- POST `/api/chat` endpoint
- Accept: message, stack_id, conversation_id (optional)
- Steps:
  1. Generate embedding for user message
  2. Search ChromaDB for relevant chunks
  3. Construct prompt with retrieved context
  4. Call OpenAI API for chat completion
  5. Return AI response with source citations

### **T8.3**: Integrate ChatKit UI
- Set up ChatKit in chat page
- Configure message rendering
- Add source citations to AI messages
- Style with Liquid Glass theme

### **T8.4**: Implement chat history
- Store conversations in Supabase
- Create `conversations` table (id, stack_id, created_at)
- Create `messages` table (id, conversation_id, role, content, sources)
- Load previous conversations in sidebar
- Allow starting new conversations

### **T8.5**: Add Pro tier gating
- Check user tier before allowing chat access
- Show upgrade prompt for free tier users
- Document Pro tier features in UI

---

## Phase 9: Testing & Validation (Week 10)

### **T9.1**: End-to-end user flow testing
- Sign up new account → Create stack → Upload documents → Search → View results
- Test with multiple document types (PDF, DOCX, TXT)
- Verify metadata generation quality
- Check processing times (<30s target)

### **T9.2**: Multi-user testing
- Create multiple test accounts
- Verify data isolation (users can't see each other's stacks/documents)
- Test RLS policies thoroughly
- Verify freemium limits enforcement

### **T9.3**: Error scenario testing
- Upload invalid files (non-PDF/DOCX/TXT)
- Upload files exceeding size limit (>50MB)
- Test with corrupted files
- Exceed freemium limits (stacks, documents, storage)
- Test network failures during upload
- Verify all error messages are user-friendly

### **T9.4**: Performance testing
- Upload 50+ documents to single stack
- Measure search response time
- Test with large files (45-50MB)
- Monitor ChromaDB performance
- Check frontend rendering performance (Liquid Glass effects)

### **T9.5**: Accessibility testing
- Keyboard navigation through all flows
- Screen reader compatibility (ARIA labels)
- Color contrast checking (WCAG AA)
- Focus states on interactive elements
- Test with browser zoom (125%, 150%)

### **T9.6**: Browser compatibility testing
- Test on Chrome, Firefox, Safari, Edge
- Verify backdrop-filter support (fallback for older browsers)
- Test on mobile browsers (iOS Safari, Chrome Mobile)
- Check for layout issues across browsers

---

## Phase 10: Documentation & Deployment (Weeks 11-12)

### **T10.1**: Create comprehensive README
- Project overview and value proposition
- Tech stack documentation
- Local development setup instructions
- Environment variables guide
- Architecture diagram
- Deployment instructions

### **T10.2**: Write API documentation
- Document all backend endpoints
- Include request/response examples
- Add error codes and messages
- Create Postman/Thunder Client collection

### **T10.3**: Add inline code comments
- Comment complex logic and architectural decisions
- Document Liquid Glass CSS patterns
- Explain RAG pipeline flow (if implemented)
- Add JSDoc comments to key functions

### **T10.4**: Create user guide
- How to create stacks
- How to upload documents
- How to search effectively
- Understanding AI-generated metadata
- Freemium vs Pro tier comparison

### **T10.5**: Set up deployment environment
- Choose hosting platform (Railway, Fly.io, or VPS)
- Configure Docker Compose for production
- Set up ChromaDB persistent storage
- Configure Supabase production settings
- Set up environment variables in hosting platform

### **T10.6**: Deploy application
- Deploy backend (FastAPI + ChromaDB)
- Deploy frontend (Next.js)
- Configure custom domain (optional)
- Set up SSL certificates
- Test deployed application end-to-end

### **T10.7**: Create demo content
- Prepare demo account with sample documents
- Create demo video showing key features
- Take screenshots for portfolio/README
- Write blog post or case study

### **T10.8**: Performance monitoring setup
- Add error tracking (Sentry or similar)
- Set up basic analytics (Vercel Analytics or similar)
- Monitor API response times
- Set up uptime monitoring

---

## Optional Enhancements (Post-MVP)

### **MCP Server Integration**
- [ ] Create MCP server endpoint for developer access
- [ ] Document MCP connection setup
- [ ] Test with Claude Desktop

### **Advanced Features**
- [ ] Document version history
- [ ] Collaborative stacks (team access)
- [ ] Batch document upload
- [ ] Export search results
- [ ] Custom embedding models (local models option)

### **Payment Integration (for v3.0)**
- [ ] Integrate Stripe
- [ ] Create pricing tiers
- [ ] Build subscription management UI
- [ ] Handle billing webhooks

---

## Notes for Development

### **Branch Strategy**
- Create `v2.0-dev` branch from `main`
- Commit after each task completion
- Create feature branches for major phases if needed
- Merge to `main` only when v2.0 is fully tested

### **Commit Message Format**
```
Complete T[X.Y]: [Brief description]

- Bullet point details of changes
- Reference related tasks if applicable
```

### **Development Workflow**
1. Check this tasks file to identify current phase
2. Complete one task at a time
3. Test task completion before moving to next
4. Update this file with `[x]` when task is done
5. Commit with proper message referencing task ID

### **Code Philosophy (from v1.0)**
- Write minimal, readable code
- Keep functions small and focused
- Prefer composition over abstraction
- Use TypeScript for type safety
- Prioritize user experience and visual polish
- Maintain clean git history

### **Design Philosophy**
- Liquid Glass effects should enhance, not hinder usability
- Test performance early and often
- Maintain accessibility standards
- Provide graceful fallbacks for older browsers
- Keep mobile experience smooth (reduce effects if needed)

---

## Current Task
**Next up:** T1.1 - Set up Supabase project

---

## Success Criteria (from PRD)

By end of 12 weeks:
- ✅ Multi-user authentication working
- ✅ Upload PDF/DOCX/TXT with AI metadata generation
- ✅ Stacks concept implemented with freemium limits
- ✅ Semantic search functional (<1s response time)
- ✅ ChromaDB self-hosted and working
- ✅ Liquid Glass UI fully implemented
- ✅ Application deployed and accessible
- ✅ Demo video created for portfolio

**Optional (if time permits):**
- ✅ Chat interface with RAG (Pro tier)
- ✅ MCP server for developer access

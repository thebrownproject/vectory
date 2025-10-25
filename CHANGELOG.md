# Changelog

All notable changes to Vectory will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Versioned documentation structure (docs/v1.0/, docs/v2.0/)
- CHANGELOG.md for release tracking
- ARCHITECTURE.md files for design decision records

---

## [1.0.0] - 2025-10-08

### Added
- **Core PDF ingestion pipeline**
  - Drag-and-drop PDF upload interface
  - Text extraction using pypdf library
  - Intelligent text chunking (1000 chars, 200 overlap) via LangChain
  - OpenAI embeddings generation (text-embedding-3-small, 1536 dimensions)
  - Vector storage in Pinecone with rich metadata

- **Vector Database Adapter Pattern**
  - Abstract base class for vector DB operations
  - Pinecone adapter implementation
  - Easy swapping via VECTOR_DB_PROVIDER environment variable

- **Frontend**
  - Next.js 15 with TypeScript and Tailwind CSS
  - FileUpload component with react-dropzone
  - StatusDisplay component with type-safe state management
  - API service layer for backend communication

- **Error Handling**
  - Comprehensive error states (400, 422, 503)
  - User-friendly error messages
  - Discriminated unions for type-safe state management

- **Metadata Tracking**
  - Filename, page number, chunk index
  - Upload timestamp (UTC)
  - Total chunks per document
  - Original text stored with each vector

- **Documentation**
  - Professional README.md with architecture diagram
  - Strategic code comments
  - Development notes with session-by-session context
  - PRD and tasks documentation

### Technical Details
- Backend: FastAPI 0.118 with Python 3.11+
- Frontend: Next.js 15 with TypeScript 5
- Vector DB: Pinecone 7.3.0
- Embeddings: OpenAI text-embedding-3-small (1536 dimensions)
- Text Processing: LangChain RecursiveCharacterTextSplitter

### Performance
- Processing time: <30 seconds for typical multi-page PDFs
- Supports PDFs up to 50MB
- Text extraction accuracy: >95% for digital PDFs

---

## [0.1.0] - 2025-10-05

### Added
- Initial project setup
- Backend FastAPI structure with CORS
- Frontend Next.js 15 structure
- Environment configuration templates

---

[Unreleased]: https://github.com/thebrownproject/vectory/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/thebrownproject/vectory/releases/tag/v1.0.0
[0.1.0]: https://github.com/thebrownproject/vectory/releases/tag/v0.1.0

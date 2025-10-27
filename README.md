# Vectory

![Status](https://img.shields.io/badge/status-complete-green)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?logo=nextdotjs&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?logo=typescript&logoColor=white)
![Pinecone](https://img.shields.io/badge/Pinecone-000000?logo=pinecone&logoColor=white)

> RAG document processing pipeline for chunking and vectorizing documents with drag-and-drop upload interface

🔗 **Live Demo:** *Coming soon*

---

## Overview

Vectory is a full-stack document ingestion pipeline that transforms PDFs into searchable vector embeddings for RAG (Retrieval-Augmented Generation) applications. Users upload documents via a drag-and-drop interface, and the system automatically extracts text, intelligently chunks content, generates embeddings via OpenAI, and stores vectors in Pinecone. Built as an exploration of RAG architecture patterns and vector database integration, demonstrating adapter pattern implementation for database portability across Pinecone, Chroma, Supabase, and Weaviate.

---

## Tech Stack

**Frontend:** Next.js 15 · TypeScript · TailwindCSS · react-dropzone
**Backend:** FastAPI · Python 3.11
**AI/ML:** LangChain · OpenAI API (text-embedding-3-small) · Pinecone
**Architecture:** Adapter Pattern · Service Layer · RESTful API

---

## Features

- Drag-and-drop PDF upload interface with real-time processing feedback
- Intelligent text chunking using LangChain RecursiveCharacterTextSplitter (1000 chars, 200 overlap)
- OpenAI embedding generation with text-embedding-3-small model (1536 dimensions)
- Adapter pattern for vector database portability enabling provider switching via environment variable
- Namespace isolation strategy using filename-uuid format for document versioning
- Rich metadata tracking including filename, page number, chunk index, and timestamp
- Type-safe state management using TypeScript discriminated unions
- Clean architecture with service layer separation and abstract base class interfaces

---

## Architecture & Tech Decisions

Built with FastAPI and Next.js to demonstrate modern full-stack architecture for AI document processing. Implemented adapter pattern with abstract base class `VectorDBAdapter` defining `upsert()` and `health_check()` methods, allowing vector database swapping without refactoring application code. Chose LangChain for text splitting due to its intelligent chunking algorithms optimized for semantic coherence. Used TypeScript discriminated unions for upload state management to enforce type-safe state transitions and prevent impossible states at compile time. Namespace strategy generates unique identifiers per upload session (`filename-uuid`) enabling document re-uploads and isolated querying. Service layer pattern separates API communication logic from React components for testability and reusability.

---

## Learnings & Challenges

**Key Learnings:**
- Implementing RAG document ingestion pipeline with LangChain text splitting and OpenAI embeddings
- Designing adapter pattern with Python abstract base classes for database-agnostic architecture
- Using TypeScript discriminated unions for exhaustive type checking and impossible state prevention
- Building clean API architecture with FastAPI including CORS configuration and error handling

**Challenges Overcome:**
- Designing adapter interface that balances simplicity with extensibility for multiple vector DB providers
- Implementing controlled component pattern in React to maintain single source of truth for file state
- Choosing optimal chunking parameters (1000 chars, 200 overlap) balancing semantic coherence with embedding costs
- Structuring metadata schema to support future query requirements without over-engineering

---

## Quick Start

```bash
# Backend setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend setup (separate terminal)
cd frontend
npm install
npm run dev
# Requires .env with OPENAI_API_KEY and PINECONE_API_KEY
```

Create `backend/.env`:
```
OPENAI_API_KEY=sk-your-key-here
PINECONE_API_KEY=your-pinecone-key
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=vectory
VECTOR_DB_PROVIDER=pinecone
```

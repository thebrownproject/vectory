from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from datetime import datetime, timezone
import uuid
import tempfile
import os

from services.pdf_processor import PDFProcessor
from services.embeddings import EmbeddingService
from adapters import PineconeAdapter


router = APIRouter(prefix="/api", tags=["upload"])


@router.post("/upload")
async def upload_pdf(files: List[UploadFile] = File(...)):
    """
    Upload and process PDF files into vector embeddings.

    Complete pipeline: PDF → Text Extraction → Chunking → Embeddings → Vector Storage

    This endpoint orchestrates the 4-step ingestion pipeline:
    1. Extract text from PDF (pypdf)
    2. Chunk text intelligently (LangChain RecursiveCharacterTextSplitter)
    3. Generate embeddings (OpenAI text-embedding-3-small)
    4. Store vectors in Pinecone with rich metadata

    Each file gets a unique namespace: {filename}-{uuid} to allow re-uploads.
    """

    # Validate file types - reject non-PDFs early
    for file in files:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {file.filename}. Only PDF files are accepted."
            )

    # Initialize services (fails fast if API keys missing)
    try:
        pdf_processor = PDFProcessor()
        embedding_service = EmbeddingService()
        vector_adapter = PineconeAdapter()
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service initialization failed: {str(e)}"
        )

    results = []

    for file in files:
        try:
            # Save uploaded file to temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                content = await file.read()
                tmp_file.write(content)
                tmp_file_path = tmp_file.name

            try:
                # STEP 1: Extract and chunk PDF
                # Extracts text page-by-page, then splits into ~1000 char chunks with 200 char overlap
                chunks = pdf_processor.process_pdf(tmp_file_path)

                if not chunks:
                    raise HTTPException(
                        status_code=422,
                        detail=f"No text could be extracted from {file.filename}"
                    )

                # STEP 2: Generate embeddings
                # Batch process all chunks through OpenAI to get 1536-dimensional vectors
                chunk_texts = [chunk["text"] for chunk in chunks]
                embeddings = embedding_service.generate_embeddings(chunk_texts)

                # STEP 3: Prepare metadata for each chunk
                # Namespace format: filename-uuid ensures uniqueness for re-uploads
                upload_timestamp = datetime.now(timezone.utc).isoformat()
                namespace = f"{file.filename}-{uuid.uuid4().hex[:8]}"

                metadata_list = []
                ids = []

                for i, chunk in enumerate(chunks):
                    chunk_id = f"{namespace}-chunk-{i}"
                    ids.append(chunk_id)

                    # Store rich metadata for future retrieval/filtering
                    metadata_list.append({
                        "filename": file.filename,
                        "page_number": chunk["page_number"],
                        "chunk_index": chunk["chunk_index"],
                        "upload_timestamp": upload_timestamp,
                        "total_chunks": len(chunks),
                        "text": chunk["text"]  # Store original text for display in search results
                    })

                # STEP 4: Upsert to vector database
                # Uses adapter pattern - swap Pinecone for Chroma/Supabase by changing VECTOR_DB_PROVIDER env var
                upsert_result = vector_adapter.upsert(
                    vectors=embeddings,
                    metadata=metadata_list,
                    namespace=namespace,
                    ids=ids
                )

                # Add to results
                results.append({
                    "filename": file.filename,
                    "chunks_created": len(chunks),
                    "vectors_stored": upsert_result["upserted_count"],
                    "namespace": namespace
                })

            finally:
                # Clean up temporary file (runs even if processing fails)
                os.unlink(tmp_file_path)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=503,
                detail=f"Processing failed for {file.filename}: {str(e)}"
            )

    return {
        "success": True,
        "files_processed": len(results),
        "results": results
    }

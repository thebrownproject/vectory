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

    Accepts one or more PDF files, extracts text, chunks it,
    generates embeddings, and stores them in Pinecone.
    """

    # Validate file types
    for file in files:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {file.filename}. Only PDF files are accepted."
            )

    # Initialize services
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
                # Step 1: Extract and chunk PDF
                chunks = pdf_processor.process_pdf(tmp_file_path)

                if not chunks:
                    raise HTTPException(
                        status_code=422,
                        detail=f"No text could be extracted from {file.filename}"
                    )

                # Step 2: Generate embeddings
                chunk_texts = [chunk["text"] for chunk in chunks]
                embeddings = embedding_service.generate_embeddings(chunk_texts)

                # Step 3: Prepare metadata for each chunk
                upload_timestamp = datetime.now(timezone.utc).isoformat()
                namespace = f"{file.filename}-{uuid.uuid4().hex[:8]}"

                metadata_list = []
                ids = []

                for i, chunk in enumerate(chunks):
                    chunk_id = f"{namespace}-chunk-{i}"
                    ids.append(chunk_id)

                    metadata_list.append({
                        "filename": file.filename,
                        "page_number": chunk["page_number"],
                        "chunk_index": chunk["chunk_index"],
                        "upload_timestamp": upload_timestamp,
                        "total_chunks": len(chunks),
                        "text": chunk["text"]
                    })

                # Step 4: Upsert to vector database
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
                # Clean up temporary file
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

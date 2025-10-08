from typing import List, Dict, Any
from pinecone import Pinecone
from .base_adapter import VectorDBAdapter
import os


class PineconeAdapter(VectorDBAdapter):
    """Pinecone implementation of the vector database adapter"""

    def __init__(self):
        self.api_key = os.getenv("PINECONE_API_KEY")
        self.index_name = os.getenv("PINECONE_INDEX_NAME", "vectory")

        if not self.api_key:
            raise ValueError("PINECONE_API_KEY environment variable not set")

        self.client = Pinecone(api_key=self.api_key)
        self.index = self.client.Index(self.index_name)

    def upsert(
        self,
        vectors: List[List[float]],
        metadata: List[Dict[str, Any]],
        namespace: str,
        ids: List[str]
    ) -> Dict[str, Any]:
        """Upsert vectors to Pinecone"""

        # Validate namespace - prevents accidental writes to default namespace
        # Each upload should have its own namespace (e.g., "document.pdf-uuid")
        if not namespace or not namespace.strip():
            raise ValueError("namespace must be a non-empty string")

        # Prepare vectors in Pinecone format: {"id": str, "values": List[float], "metadata": dict}
        # This format allows Pinecone to index vectors and filter by metadata
        pinecone_vectors = [
            {
                "id": ids[i],
                "values": vectors[i],  # 1536-dimensional embedding from OpenAI
                "metadata": metadata[i]  # Includes filename, page_number, chunk_index, text
            }
            for i in range(len(vectors))
        ]

        # Upsert to Pinecone (update if ID exists, insert if new)
        upsert_response = self.index.upsert(
            vectors=pinecone_vectors,
            namespace=namespace
        )

        return {
            "upserted_count": upsert_response.upserted_count
        }

    def health_check(self) -> bool:
        """Check Pinecone connection health"""
        try:
            # Check if index exists and is accessible
            self.index.describe_index_stats()
            return True
        except Exception as e:
            print(f"Pinecone health check failed: {e}")
            return False

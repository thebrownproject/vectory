from abc import ABC, abstractmethod
from typing import List, Dict, Any


class VectorDBAdapter(ABC):
    """Base adapter interface for vector database operations"""

    @abstractmethod
    def upsert(
        self,
        vectors: List[List[float]],
        metadata: List[Dict[str, Any]],
        namespace: str,
        ids: List[str]
    ) -> Dict[str, Any]:
        """
        Upsert vectors to the vector database

        Args:
            vectors: List of embedding vectors (each should be 1536 dimensions for text-embedding-3-small)
            metadata: List of metadata dictionaries (one per vector)
            namespace: Namespace to store vectors in (typically filename-based)
            ids: List of unique identifiers for each vector

        Returns:
            Dict with upsert result stats (e.g., {'upserted_count': 45})
        """
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """
        Check if the vector database connection is healthy

        Returns:
            True if connection is healthy, False otherwise
        """
        pass

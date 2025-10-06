import os
from openai import OpenAI
from typing import List


class EmbeddingService:
    """Generate embeddings using OpenAI's text-embedding-3-small model."""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        self.client = OpenAI(api_key=api_key)
        self.model = "text-embedding-3-small"
        self.dimensions = 1536

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of text chunks.

        Args:
            texts: List of text strings to embed (max 2048 per batch)

        Returns:
            List of embedding vectors (each is a list of 1536 floats)

        Raises:
            Exception: If OpenAI API call fails
        """
        if not texts:
            return []

        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=texts
            )

            # Extract embeddings maintaining order
            embeddings = [item.embedding for item in response.data]
            return embeddings

        except Exception as e:
            raise Exception(f"Failed to generate embeddings: {str(e)}")

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text string.

        Args:
            text: Text string to embed

        Returns:
            Embedding vector (list of 1536 floats)
        """
        embeddings = self.generate_embeddings([text])
        return embeddings[0]

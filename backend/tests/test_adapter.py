"""
Development utility - not part of production code
Simple test script for Pinecone adapter
Run this after configuring PINECONE_API_KEY in .env
"""
import os
import sys
from pathlib import Path

# Add parent directory to path so we can import from backend
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from adapters import PineconeAdapter

load_dotenv()

def test_pinecone_adapter():
    print("Testing Pinecone Adapter...")

    # Check if API key is configured
    if not os.getenv("PINECONE_API_KEY"):
        print("❌ PINECONE_API_KEY not configured in .env")
        print("⚠️  This test requires a valid Pinecone API key")
        return

    try:
        # Initialize adapter
        adapter = PineconeAdapter()
        print("✅ Adapter initialized successfully")

        # Test health check
        is_healthy = adapter.health_check()
        if is_healthy:
            print("✅ Pinecone connection healthy")
        else:
            print("❌ Pinecone connection failed")
            return

        # Test upsert with sample vector (1536 dimensions for text-embedding-3-small)
        sample_vector = [[0.1] * 1536]  # Single sample vector
        sample_metadata = [{
            "filename": "test.pdf",
            "page_number": 1,
            "chunk_index": 0,
            "text": "This is a test chunk"
        }]
        sample_ids = ["test-vector-1"]

        result = adapter.upsert(
            vectors=sample_vector,
            metadata=sample_metadata,
            namespace="test",
            ids=sample_ids
        )

        print(f"✅ Upsert successful: {result}")

    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_pinecone_adapter()

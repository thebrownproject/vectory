#!/usr/bin/env python3
"""
Test script for EmbeddingService
Tests both single and batch embedding generation
"""

import os
from dotenv import load_dotenv
from services.embeddings import EmbeddingService

# Load environment variables
load_dotenv()

def test_single_embedding():
    """Test generating a single embedding"""
    print("=" * 50)
    print("Testing single embedding generation...")
    print("=" * 50)

    service = EmbeddingService()
    text = "This is a test sentence for embedding generation."

    embedding = service.generate_embedding(text)

    print(f"Input text: {text}")
    print(f"Embedding dimensions: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")
    print(f"Expected dimensions: {service.dimensions}")

    assert len(embedding) == 1536, f"Expected 1536 dimensions, got {len(embedding)}"
    print("✓ Single embedding test passed!\n")

def test_batch_embeddings():
    """Test generating multiple embeddings at once"""
    print("=" * 50)
    print("Testing batch embedding generation...")
    print("=" * 50)

    service = EmbeddingService()
    texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Machine learning is a subset of artificial intelligence.",
        "Python is a popular programming language for data science.",
    ]

    embeddings = service.generate_embeddings(texts)

    print(f"Number of texts: {len(texts)}")
    print(f"Number of embeddings: {len(embeddings)}")
    print(f"Each embedding dimensions: {len(embeddings[0])}")

    for i, text in enumerate(texts):
        print(f"\nText {i+1}: {text[:50]}...")
        print(f"  Embedding preview: {embeddings[i][:3]}")

    assert len(embeddings) == len(texts), "Mismatch between input and output counts"
    assert all(len(emb) == 1536 for emb in embeddings), "Inconsistent embedding dimensions"
    print("\n✓ Batch embedding test passed!\n")

def test_empty_input():
    """Test handling of empty input"""
    print("=" * 50)
    print("Testing empty input handling...")
    print("=" * 50)

    service = EmbeddingService()
    embeddings = service.generate_embeddings([])

    assert embeddings == [], "Expected empty list for empty input"
    print("✓ Empty input test passed!\n")

if __name__ == "__main__":
    try:
        test_single_embedding()
        test_batch_embeddings()
        test_empty_input()

        print("=" * 50)
        print("ALL TESTS PASSED! ✓")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        raise

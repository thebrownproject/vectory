"""
Development utility - not part of production code
Simple test script for PDF processor
Run this to verify PDF extraction and chunking
"""
from services.pdf_processor import PDFProcessor


def test_pdf_processor():
    print("Testing PDF Processor...")

    # Path to sample PDF
    pdf_path = "/Users/fraserbrown/Library/CloudStorage/OneDrive-Personal/Desktop/11 Empress Ave, Kingville - 2025.09.23 - BS prelim package/Soil Report/Soil Report - 250046.pdf"

    try:
        # Initialize processor with default settings
        processor = PDFProcessor(chunk_size=1000, chunk_overlap=200)
        print("✅ PDFProcessor initialized (chunk_size=1000, overlap=200)")

        # Extract text with page tracking
        print("\n📄 Extracting text from PDF...")
        pages_data = processor.extract_text_with_pages(pdf_path)
        print(f"✅ Extracted {len(pages_data)} pages with text content")

        # Chunk the text
        print("\n✂️  Chunking text...")
        chunks = processor.chunk_text(pages_data)
        print(f"✅ Created {len(chunks)} chunks")

        # Display sample chunk
        if chunks:
            print("\n📝 Sample chunk (first chunk):")
            print("-" * 60)
            sample = chunks[0]
            print(f"Page Number: {sample['page_number']}")
            print(f"Chunk Index: {sample['chunk_index']}")
            print(f"Text Length: {len(sample['text'])} characters")
            print(f"Text Preview:\n{sample['text'][:200]}...")
            print("-" * 60)

        # Display stats
        print("\n📊 Processing Statistics:")
        print(f"   Total pages: {len(pages_data)}")
        print(f"   Total chunks: {len(chunks)}")
        print(f"   Avg chunks per page: {len(chunks) / len(pages_data):.1f}")

        # Test the combined process_pdf method
        print("\n🔄 Testing combined process_pdf() method...")
        all_chunks = processor.process_pdf(pdf_path)
        print(f"✅ process_pdf() returned {len(all_chunks)} chunks")

        print("\n✅ All tests passed!")

    except FileNotFoundError:
        print(f"❌ PDF file not found at: {pdf_path}")
        print("⚠️  Please check the file path and try again")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_pdf_processor()

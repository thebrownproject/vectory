"""
Test script for the upload endpoint.

This script tests the complete upload pipeline:
1. Starts the FastAPI server (requires manual start)
2. Uploads a test PDF
3. Verifies the response

Prerequisites:
- Backend server running: uvicorn main:app --reload --port 8000
- Valid API keys in .env file
- Test PDF file available
"""

import requests
import os

# Configuration
API_URL = "http://localhost:8000/api/upload"
TEST_PDF_PATH = "test_data/Building_Surveyors_Referral_Response_Report.pdf"

def test_upload():
    """Test PDF upload endpoint"""

    # Check if test PDF exists
    if not os.path.exists(TEST_PDF_PATH):
        print(f"❌ Test PDF not found at: {TEST_PDF_PATH}")
        print("Please ensure test PDF is available")
        return

    print(f"📄 Testing upload with: {TEST_PDF_PATH}")

    # Prepare file for upload
    with open(TEST_PDF_PATH, 'rb') as f:
        files = {'files': (os.path.basename(TEST_PDF_PATH), f, 'application/pdf')}

        print("📤 Uploading PDF to FastAPI endpoint...")

        try:
            response = requests.post(API_URL, files=files, timeout=60)

            # Check response
            if response.status_code == 200:
                data = response.json()
                print("\n✅ Upload successful!")
                print(f"   Files processed: {data['files_processed']}")

                for result in data['results']:
                    print(f"\n   📊 Results for {result['filename']}:")
                    print(f"      - Chunks created: {result['chunks_created']}")
                    print(f"      - Vectors stored: {result['vectors_stored']}")
                    print(f"      - Namespace: {result['namespace']}")
            else:
                print(f"\n❌ Upload failed with status code: {response.status_code}")
                print(f"   Response: {response.text}")

        except requests.exceptions.ConnectionError:
            print("\n❌ Connection failed!")
            print("   Make sure the backend server is running:")
            print("   cd backend && uvicorn main:app --reload --port 8000")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    print("=" * 60)
    print("Vectory Upload Endpoint Test")
    print("=" * 60)
    test_upload()
    print("\n" + "=" * 60)

// API service for backend communication

interface UploadResult {
  filename: string;
  chunks_created: number;
  vectors_stored: number;
  namespace: string;
}

interface UploadResponse {
  success: boolean;
  files_processed: number;
  results: UploadResult[];
}

/**
 * Upload PDF files to the FastAPI backend for processing
 * @param files Array of PDF files to upload
 * @returns Upload results with chunk and vector counts
 * @throws Error if upload fails
 */
export async function uploadPDFs(files: File[]): Promise<UploadResult[]> {
  if (files.length === 0) {
    throw new Error("No files provided");
  }

  const formData = new FormData();
  files.forEach((file) => {
    formData.append("files", file);
  });

  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/api/upload`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({
      detail: "Upload failed",
    }));
    throw new Error(
      errorData.detail || `Upload failed with status ${response.status}`
    );
  }

  const data: UploadResponse = await response.json();
  return data.results;
}

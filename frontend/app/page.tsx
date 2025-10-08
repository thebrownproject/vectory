"use client";

import { useState } from "react";
import FileUpload from "@/components/FileUpload";
import StatusDisplay, { UploadStatus } from "@/components/StatusDisplay";
import { uploadPDFs } from "@/lib/api";

export default function Home() {
  // State management using controlled component pattern
  // files: Managed here (single source of truth), passed down to FileUpload
  // uploadStatus: Discriminated union prevents impossible states (e.g., error + success simultaneously)
  const [files, setFiles] = useState<File[]>([]);
  const [uploadStatus, setUploadStatus] = useState<UploadStatus>({
    state: "idle",
  });

  const handleUpload = async () => {
    if (files.length === 0) return;

    setUploadStatus({ state: "uploading", filesCount: files.length });

    try {
      const results = await uploadPDFs(files);

      setUploadStatus({
        state: "success",
        results,
      });

      // Clear files after successful upload (ready for next batch)
      setFiles([]);
    } catch (error) {
      setUploadStatus({
        state: "error",
        message:
          error instanceof Error
            ? error.message
            : "An unexpected error occurred",
      });
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Vectory</h1>
          <p className="text-gray-600">
            Upload PDFs to generate and store vector embeddings
          </p>
        </div>

        {/* Main content */}
        <div className="bg-white rounded-lg shadow-sm p-6 space-y-6">
          {/* Controlled component: parent manages files state, child receives props */}
          <FileUpload
            files={files}
            onFilesChange={setFiles}
            disabled={uploadStatus.state === "uploading"}
          />

          {/* Upload button */}
          {files.length > 0 && (
            <button
              type="button"
              onClick={handleUpload}
              disabled={uploadStatus.state === "uploading"}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400
                       text-white font-medium py-3 px-4 rounded-lg
                       transition-colors disabled:cursor-not-allowed"
            >
              {uploadStatus.state === "uploading"
                ? "Processing..."
                : `Upload ${files.length} ${files.length === 1 ? "File" : "Files"}`}
            </button>
          )}

          {/* Status display */}
          <StatusDisplay status={uploadStatus} />
        </div>
      </div>
    </div>
  );
}

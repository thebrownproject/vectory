"use client";

import React from "react";
import { CheckCircle, XCircle, Loader2, FileText } from "lucide-react";

// Type for upload status - using discriminated union for type safety
export type UploadStatus =
  | { state: "idle" }
  | { state: "uploading"; filesCount: number }
  | {
      state: "success";
      results: Array<{
        filename: string;
        chunks_created: number;
        vectors_stored: number;
        namespace: string;
      }>;
    }
  | { state: "error"; message: string };

interface StatusDisplayProps {
  status: UploadStatus;
}

export default function StatusDisplay({ status }: StatusDisplayProps) {
  // Idle state - nothing to show
  if (status.state === "idle") {
    return null;
  }

  // Uploading state - show spinner
  if (status.state === "uploading") {
    return (
      <div className="w-full p-6 bg-blue-50 border border-blue-200 rounded-lg">
        <div className="flex items-center space-x-3">
          <Loader2 className="w-6 h-6 text-blue-600 animate-spin" />
          <div>
            <h3 className="text-sm font-medium text-blue-900">
              Processing Files...
            </h3>
            <p className="text-xs text-blue-700 mt-1">
              Uploading {status.filesCount}{" "}
              {status.filesCount === 1 ? "file" : "files"} and generating
              embeddings
            </p>
          </div>
        </div>
      </div>
    );
  }

  // Error state - show error message
  if (status.state === "error") {
    return (
      <div className="w-full p-6 bg-red-50 border border-red-200 rounded-lg">
        <div className="flex items-start space-x-3">
          <XCircle className="w-6 h-6 text-red-600 flex-shrink-0 mt-0.5" />
          <div className="flex-1">
            <h3 className="text-sm font-medium text-red-900">Upload Failed</h3>
            <p className="text-xs text-red-700 mt-1">{status.message}</p>
          </div>
        </div>
      </div>
    );
  }

  // Success state - show results
  return (
    <div className="w-full p-6 bg-green-50 border border-green-200 rounded-lg">
      <div className="flex items-start space-x-3 mb-4">
        <CheckCircle className="w-6 h-6 text-green-600 flex-shrink-0 mt-0.5" />
        <div className="flex-1">
          <h3 className="text-sm font-medium text-green-900">
            Upload Successful!
          </h3>
          <p className="text-xs text-green-700 mt-1">
            {status.results.length}{" "}
            {status.results.length === 1 ? "file" : "files"} processed and
            stored in vector database
          </p>
        </div>
      </div>

      {/* Results breakdown */}
      <div className="space-y-3 mt-4">
        {status.results.map((result) => (
          <div
            key={result.namespace}
            className="bg-white p-4 rounded-lg border border-green-200"
          >
            <div className="flex items-start space-x-3">
              <FileText className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 truncate">
                  {result.filename}
                </p>
                <div className="mt-2 grid grid-cols-2 gap-3 text-xs">
                  <div>
                    <span className="text-gray-500">Chunks created:</span>
                    <span className="ml-2 font-medium text-gray-900">
                      {result.chunks_created}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-500">Vectors stored:</span>
                    <span className="ml-2 font-medium text-gray-900">
                      {result.vectors_stored}
                    </span>
                  </div>
                </div>
                <div className="mt-2 text-xs">
                  <span className="text-gray-500">Namespace:</span>
                  <code className="ml-2 px-2 py-0.5 bg-gray-100 rounded text-gray-700 font-mono">
                    {result.namespace}
                  </code>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

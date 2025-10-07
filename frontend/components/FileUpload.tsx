"use client";

import React from "react";
import { useDropzone } from "react-dropzone";
import { Upload, X, FileText } from "lucide-react";

interface FileUploadProps {
  files: File[];
  onFilesChange: (files: File[]) => void;
  disabled?: boolean;
}

export default function FileUpload({
  files,
  onFilesChange,
  disabled = false,
}: FileUploadProps) {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      "application/pdf": [".pdf"],
    },
    onDrop: (acceptedFiles) => {
      const newFiles = [...files, ...acceptedFiles];
      onFilesChange(newFiles);
    },
    disabled,
  });

  return (
    <div className="w-full space-y-4">
      {/* Dropzone area */}
      <div
        {...getRootProps({
          className: `
            border-2 border-dashed rounded-lg p-8
            flex flex-col items-center justify-center
            cursor-pointer transition-colors
            ${
              isDragActive
                ? "border-blue-500 bg-blue-50"
                : "border-gray-300 hover:border-gray-400"
            }
            ${disabled ? "opacity-50 cursor-not-allowed" : ""}
          `,
        })}
      >
        <input {...getInputProps()} />
        <Upload className="w-12 h-12 text-gray-400 mb-4" />
        <p className="text-sm text-gray-600 text-center">
          {isDragActive
            ? "Drop the PDFs here..."
            : "Drag & drop PDFs here, or click to browse"}
        </p>
        <p className="text-xs text-gray-400 mt-2">PDF files only</p>
      </div>

      {/* Selected files list */}
      {files.length > 0 && (
        <div className="space-y-2">
          <h4 className="text-sm font-medium text-gray-700">
            Selected Files ({files.length})
          </h4>
          {files.map((file, index) => (
            <div
              key={`${file.name}-${index}`}
              className="flex items-center justify-between p-3 bg-gray-50
  rounded-lg border border-gray-200"
            >
              <div className="flex items-center space-x-3">
                <FileText className="w-5 h-5 text-blue-500" />
                <div>
                  <p className="text-sm font-medium text-gray-900">
                    {file.name}
                  </p>
                  <p className="text-xs text-gray-500">
                    {(file.size / 1024).toFixed(2)} KB
                  </p>
                </div>
              </div>
              <button
                onClick={() => {
                  onFilesChange(files.filter((_, i) => i !== index));
                }}
                className="text-gray-400 hover:text-red-500 transition-colors"
                type="button"
                aria-label={`Remove ${file.name}`}
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

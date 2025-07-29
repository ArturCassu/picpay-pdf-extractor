"use client"
import React, { useState } from "react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<any>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFile(e.target.files?.[0] || null);
    setResult(null);
    setError("");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError("Please select a PDF file.");
      return;
    }
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const formData = new FormData();
      formData.append("file", file);
      // TODO: Replace with your FastAPI backend URL
      const response = await fetch("http://localhost:8000/extract", {
        method: "POST",
        body: formData,
      });
      if (!response.ok) throw new Error("Failed to extract PDF");
      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 py-10">
      <h1 className="text-3xl font-bold mb-6">PDF Extractor</h1>
      <form
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded shadow-md flex flex-col gap-4 w-full max-w-md"
      >
        <input
          type="file"
          accept="application/pdf"
          onChange={handleFileChange}
          className="border p-2 rounded"
        />
        <button
          type="submit"
          className="bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:opacity-50"
          disabled={loading}
        >
          {loading ? "Extracting..." : "Upload & Extract"}
        </button>
        {error && <div className="text-red-600">{error}</div>}
      </form>
      {result && (
        <div className="mt-8 w-full max-w-2xl bg-white p-6 rounded shadow">
          <h2 className="text-xl font-semibold mb-2">Extracted Data</h2>
          <pre className="whitespace-pre-wrap break-words text-sm bg-gray-100 p-4 rounded overflow-x-auto">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}

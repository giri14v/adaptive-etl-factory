import { useState } from "react";

export default function UrlInput({ onRun, loading }) {
  const [url, setUrl] = useState("");

  return (
    <div className="space-y-4">
      <input
        className="w-full border p-2 rounded"
        placeholder="Paste dataset CSV URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />

      <button
        onClick={() => onRun(url)}
        disabled={loading || !url}
        className="w-full bg-blue-600 text-white py-2 rounded disabled:opacity-50"
      >
        {loading ? "Running ETL..." : "Run ETL"}
      </button>
    </div>
  );
}

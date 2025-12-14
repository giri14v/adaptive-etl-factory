export default function StatusPanel({ runId, loading, error }) {
  if (error) {
    return (
      <div className="mt-4 bg-red-100 border border-red-300 p-3 rounded">
        {error}
      </div>
    );
  }

  if (!runId) return null;

  return (
    <div className="mt-4 bg-blue-50 border p-3 rounded">
      <p className="font-semibold">Run ID</p>
      <p className="text-sm break-all">{runId}</p>
      {loading && <p className="mt-2 text-blue-600">Processing…</p>}
    </div>
  );
}

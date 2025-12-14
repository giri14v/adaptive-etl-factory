export default function ResultPanel({ metrics, downloadUrl }) {
  if (!metrics) return null;
  return (
    <div className="mt-6 bg-green-50 border p-4 rounded">
      <h3 className="text-lg font-bold text-green-700">
        Results Summary
      </h3>

      <p className="text-green-700 font-semibold">
        Quality Score:{" "}
        <span className="font-bold">
          {(metrics.quality_score * 100).toFixed(1)}%
        </span>
      </p>

      <p>Rows: {metrics.rows}</p>
      <p>Columns: {metrics.columns}</p>
      <p>Null Density: {metrics.null_density}</p>

      <a
        href={downloadUrl}
        download
        className="inline-block mt-4 bg-green-600 text-white px-4 py-2 rounded"
      >
        Download Cleaned CSV
      </a>
    </div>
  );
}

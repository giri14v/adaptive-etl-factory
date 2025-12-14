const BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function runETL(fileUrl) {
  const res = await fetch(`${BASE_URL}/run-etl`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ file_url: fileUrl }),
  });

  if (!res.ok) throw new Error("Failed to start ETL");
  return res.json();
}

export async function fetchMetrics(runId) {
  const res = await fetch(`${BASE_URL}/results/${runId}/metrics`);
  if (!res.ok) throw new Error("Metrics not ready");
  return res.json();
}

export function outputCsvUrl(runId) {
  return `${BASE_URL}/results/${runId}/output`;
}

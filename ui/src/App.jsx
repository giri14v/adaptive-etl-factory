import { useState } from "react";
import Header from "./components/Header";
import UrlInput from "./components/UrlInput";
import StatusPanel from "./components/StatusPanel";
import ResultPanel from "./components/ResultPanel";
import { runETL, fetchMetrics, outputCsvUrl } from "./api/etl";

function App() {
  const [runId, setRunId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [metrics, setMetrics] = useState(null);
  const [error, setError] = useState(null);

  const handleRun = async (fileUrl) => {
    setLoading(true);
    setMetrics(null);
    setError(null);

    try {
      const res = await runETL(fileUrl);
      setRunId(res.execution_id);
      // simple polling (hackathon-safe)
      const pollMetrics = async (runId, retries = 30) => {
  try {
    const m = await fetchMetrics(runId);
    setMetrics(m);
    setLoading(false);
  } catch (err) {
    if (retries > 0) {
      setTimeout(() => pollMetrics(runId, retries - 1), 2000);
    } else {
      setLoading(false);
      setError("Evaluation not ready yet");
    }
  }
};

// after runETL success
pollMetrics(res.execution_id);

    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <div className="max-w-xl mx-auto mt-8 px-4">
        <UrlInput onRun={handleRun} loading={loading} />

        <StatusPanel runId={runId} loading={loading} error={error} />

        {metrics && (
          <ResultPanel
            metrics={metrics}
            downloadUrl={outputCsvUrl(runId)}
          />
        )}
      </div>
    </div>
  );
}

export default App;

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).end();

  const run_id = `run-${Date.now()}`;

  res.status(200).json({
    run_id,
    message: "Dataset onboarded. ETL Pipeline execution started.",
  });
}

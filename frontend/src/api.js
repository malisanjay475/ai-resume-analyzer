// Sends the resume and job description to the Flask API and returns the analysis.
export async function analyzeResume(file, jobDescription) {
  const form = new FormData();
  form.append("resume", file);
  form.append("job_description", jobDescription);

  let response;
  try {
    response = await fetch("/api/analyze", { method: "POST", body: form });
  } catch {
    throw new Error("Cannot reach the server. Is the Flask backend running?");
  }

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.error || `Something went wrong (error ${response.status}).`);
  }
  return data;
}

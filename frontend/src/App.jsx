import { useState } from "react";
import { analyzeResume } from "./api.js";
import UploadPanel from "./components/UploadPanel.jsx";
import Results from "./components/Results.jsx";

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAnalyze(file, jobText) {
    setLoading(true);
    setError("");
    try {
      setResult(await analyzeResume(file, jobText));
    } catch (err) {
      setResult(null);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <header className="header">
        <div className="brand">
          <span className="logo-dot" />
          <span>
            AI Resume <span className="gradient">Analyzer</span>
          </span>
        </div>
        <span className="pill">NLP · TF-IDF · Cosine similarity</span>
      </header>

      <main className="layout">
        <UploadPanel onAnalyze={handleAnalyze} loading={loading} />

        <div className="right">
          {error && <div className="card error-card">{error}</div>}
          {loading && <div className="card empty"><div className="spinner" />Reading your resume…</div>}
          {!loading && result && <Results result={result} />}
          {!loading && !result && !error && (
            <div className="card empty">
              <div className="empty-ring" />
              <h2>Your results will appear here</h2>
              <p className="muted">
                Upload a resume and paste a job description to see your match score, matched and missing
                skills, and tips to improve.
              </p>
            </div>
          )}
        </div>
      </main>

      <footer className="footer">Minor Project · BCA · Chandigarh University</footer>
    </div>
  );
}

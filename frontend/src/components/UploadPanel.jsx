import { useRef, useState } from "react";

const MAX_MB = 5;

const SAMPLE_JOB = `Junior Python Developer (Fresher)

Responsibilities:
- Build and maintain backend services using Python and Flask or Django.
- Design REST API endpoints and integrate them with a React frontend.
- Write efficient SQL queries for MySQL or PostgreSQL databases.
- Write unit tests and take part in code reviews using Git and GitHub.
- Deploy services with Docker on AWS.

Requirements:
- Strong knowledge of Python, data structures and OOP.
- Familiarity with HTML, CSS and JavaScript.
- Understanding of Agile development.
- Good communication and teamwork skills.`;

export default function UploadPanel({ onAnalyze, loading }) {
  const [file, setFile] = useState(null);
  const [jobText, setJobText] = useState("");
  const [dragging, setDragging] = useState(false);
  const [localError, setLocalError] = useState("");
  const inputRef = useRef(null);

  function pickFile(selected) {
    setLocalError("");
    if (!selected) return;
    if (!selected.name.toLowerCase().endsWith(".pdf")) {
      setLocalError("Only PDF files are allowed.");
      return;
    }
    if (selected.size > MAX_MB * 1024 * 1024) {
      setLocalError(`File too large. The maximum size is ${MAX_MB} MB.`);
      return;
    }
    setFile(selected);
  }

  function handleDrop(event) {
    event.preventDefault();
    setDragging(false);
    pickFile(event.dataTransfer.files[0]);
  }

  function handleSubmit(event) {
    event.preventDefault();
    if (!file) return setLocalError("Please upload your resume as a PDF file.");
    if (!jobText.trim()) return setLocalError("Please paste the job description.");
    setLocalError("");
    onAnalyze(file, jobText);
  }

  return (
    <form className="card upload" onSubmit={handleSubmit}>
      <h2 className="card-title">
        <span className="step">1</span> Upload your resume
      </h2>

      <div
        className={`dropzone ${dragging ? "dragging" : ""} ${file ? "has-file" : ""}`}
        onClick={() => inputRef.current.click()}
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => e.key === "Enter" && inputRef.current.click()}
      >
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf,.pdf"
          hidden
          onChange={(e) => pickFile(e.target.files[0])}
        />
        <svg width="44" height="44" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path d="M12 16V4m0 0l-5 5m5-5l5 5M4 20h16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
        {file ? (
          <p className="file-name">{file.name}</p>
        ) : (
          <p>
            <strong>Drop your PDF here</strong> or click to browse
          </p>
        )}
        <p className="hint">PDF only · max {MAX_MB} MB · never stored</p>
      </div>

      <h2 className="card-title">
        <span className="step">2</span> Paste the job description
        <button type="button" className="link-btn" onClick={() => setJobText(SAMPLE_JOB)}>
          Use sample
        </button>
      </h2>
      <textarea
        value={jobText}
        onChange={(e) => setJobText(e.target.value)}
        placeholder="Paste the full job description here…"
        rows={9}
      />

      {localError && <p className="error">{localError}</p>}

      <button className="primary" type="submit" disabled={loading}>
        {loading ? "Analyzing…" : "Analyze my resume"}
      </button>
    </form>
  );
}

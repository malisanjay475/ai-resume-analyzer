"""
Flask REST API for the AI Resume Analyzer.

Endpoints
  GET  /api/health    -> {"status": "ok"}
  POST /api/analyze   -> multipart form: resume (PDF file), job_description (text)

Uploaded files are processed in memory and never saved.
"""

import os

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from analyzer import ResumeReadError, analyze, extract_text

MAX_FILE_MB = 5
MAX_FILE_BYTES = MAX_FILE_MB * 1024 * 1024
MIN_JOB_CHARS = 30

FRONTEND_DIST = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")

app = Flask(__name__, static_folder=None)
# Whole request limit: the 5 MB file plus room for the job description text.
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_BYTES + 200 * 1024
CORS(app)


def error(message: str, status: int):
    return jsonify({"error": message}), status


@app.errorhandler(413)
def too_large(_err):
    return error(f"File too large. The maximum size is {MAX_FILE_MB} MB.", 413)


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/analyze")
def analyze_resume():
    upload = request.files.get("resume")
    job_text = (request.form.get("job_description") or "").strip()

    # --- validation (test cases TC02, TC03, TC06) ---
    if upload is None or not upload.filename:
        return error("Please upload your resume as a PDF file.", 400)

    data = upload.read()
    if not upload.filename.lower().endswith(".pdf") or not data.startswith(b"%PDF"):
        return error("Only PDF files are allowed. Please upload your resume as a PDF.", 400)
    if len(data) > MAX_FILE_BYTES:
        return error(f"File too large. The maximum size is {MAX_FILE_MB} MB.", 413)
    if not job_text:
        return error("Please paste the job description.", 400)
    if len(job_text) < MIN_JOB_CHARS:
        return error("The job description is too short. Please paste the full description.", 400)

    # --- analysis (TC01, TC04, TC05) ---
    try:
        resume_text = extract_text(data)
    except ResumeReadError as exc:
        return error(str(exc), 422)

    return jsonify(analyze(resume_text, job_text))


# --- serve the built React app (frontend/dist) from the same server ---
@app.get("/")
@app.get("/<path:path>")
def frontend(path="index.html"):
    if not os.path.isdir(FRONTEND_DIST):
        return "Frontend not built yet. Run: cd frontend && npm install && npm run build", 200
    if os.path.isfile(os.path.join(FRONTEND_DIST, path)):
        return send_from_directory(FRONTEND_DIST, path)
    return send_from_directory(FRONTEND_DIST, "index.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

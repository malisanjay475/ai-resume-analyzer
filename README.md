# AI Resume Analyzer

A web application that compares a resume (PDF) with a job description using Natural Language Processing, and shows a match score, matched and missing skills, and tips to improve.

**Minor Project · BCA · Chandigarh University**
Sanjay · UID O22BCA16074

---

## Features

- Upload a resume as a PDF (drag and drop or click), paste any job description
- **Match score (0–100%)** with a label: Low, Fair, Good or Strong match
- **Matched skills** and **missing skills**, from a dictionary of about 100 skills
- Understands "X **or** Y" in job descriptions (for example "Flask or Django") as one requirement
- **Suggestions**: missing skills, missing sections, resume length, numbers that show impact, contact links
- Files are processed in memory and **never stored**
- Validation: PDF only, 5 MB limit, job description required
- Works on desktop and mobile

## Tech stack

| Part | Technology | Why |
|---|---|---|
| Frontend | React 18 + Vite | Fast, component-based UI |
| Backend | Python + Flask | Lightweight REST API; Python has the best NLP libraries |
| PDF reading | pdfplumber | Reliable text extraction |
| Skill extraction | spaCy PhraseMatcher | Fast matching of skill names and their aliases |
| Similarity | scikit-learn (TF-IDF + cosine similarity) | Standard information-retrieval method |
| Testing | pytest | 13 automated tests, including TC01–TC06 |

## How the score is calculated

1. **Text extraction:** pdfplumber reads the text from every page of the PDF.
2. **Skill extraction:** spaCy's PhraseMatcher finds skills from `backend/skills.py` in both texts. Short or everyday words (Go, C, REST, Excel) only count in their proper case, so "go to the rest of" is not read as a skill.
3. **Skill coverage** = requirements met ÷ requirements in the job description.
4. **Text similarity:** both texts become TF-IDF vectors and we take the cosine of the angle between them: cos θ = (A · B) / (‖A‖ ‖B‖).
5. **Match score = 60% × skill coverage + 40% × text similarity.** Skills get more weight because that is what recruiters and ATS software filter on.

## Folder structure

```
ai-resume-analyzer/
├── backend/
│   ├── app.py            # Flask API (+ serves the built frontend)
│   ├── analyzer.py       # NLP engine: extraction, skills, TF-IDF, score, tips
│   ├── skills.py         # skills dictionary with aliases
│   ├── requirements.txt
│   └── tests/test_app.py # TC01–TC06 + unit tests
├── frontend/
│   ├── src/App.jsx
│   ├── src/api.js
│   ├── src/components/   # UploadPanel, ScoreRing, Results
│   ├── src/styles.css
│   └── dist/             # built frontend (Flask serves this)
├── samples/
│   ├── make_samples.py   # creates the sample resumes and job description
│   └── job_description.txt
├── run.bat / run.sh      # one-click start
└── VIVA_NOTES.md         # likely viva questions with answers
```

## How to run

You need **Python 3.10 or newer**. Node.js is only needed to build or change the frontend.

### Quick start (Windows)

Double-click `run.bat`, wait for it to finish installing, then open **http://127.0.0.1:5000** in your browser.

### Quick start (Mac / Linux)

```bash
bash run.sh
```

### If you cloned this from GitHub

The repository holds the source only. Before the first run, create the sample files and build the frontend once (needs Node.js 18+):

```bash
python samples/make_samples.py      # needs: pip install reportlab
cd frontend
npm install
npm run build                       # creates frontend/dist, which Flask serves
```

Then use `run.bat` / `run.sh` or the manual steps below.

### Manual steps

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac / Linux
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000**. Click **Use sample** to fill in a job description, and upload `samples/sample_resume.pdf` to try it.

### Changing the frontend (optional)

```bash
cd frontend
npm install
npm run dev        # live-reload version at http://localhost:5173 (keep app.py running too)
npm run build      # rebuild frontend/dist so Flask serves your changes
```

## Run the tests

```bash
cd backend
python -m pytest -v
```

Expected: **13 passed**.

| ID | Input | Expected output | Test |
|---|---|---|---|
| TC01 | Valid PDF resume | Text extracted | `test_tc01_valid_pdf_text_extracted` |
| TC02 | Upload a .jpg file | Error: PDF only | `test_tc02_jpg_rejected` |
| TC03 | Empty job description | Error: field required | `test_tc03_empty_job_description` |
| TC04 | Matching resume and job | High score (50% or more) | `test_tc04_matching_resume_scores_high` |
| TC05 | Unrelated resume and job | Low score (under 30%) | `test_tc05_unrelated_resume_scores_low` |
| TC06 | File over 5 MB | Error: file too large | `test_tc06_file_over_5mb_rejected` |

## API

`POST /api/analyze` (multipart form)

| Field | Type | Required |
|---|---|---|
| `resume` | PDF file, max 5 MB | yes |
| `job_description` | text, at least 30 characters | yes |

Response:

```json
{
  "score": 50,
  "label": "Good match",
  "skill_coverage": 63,
  "text_similarity": 30,
  "matched_skills": ["CSS", "Flask", "Python", "..."],
  "missing_skills": ["AWS", "Docker", "..."],
  "extra_skills": ["Algorithms"],
  "word_count": 168,
  "suggestions": ["Add these skills from the job description if you have them: ..."]
}
```

Errors return `{"error": "message"}` with status 400 (bad input), 413 (file too large) or 422 (no readable text, e.g. a scanned PDF).

## Limitations and future scope

- Scanned (image) PDFs are not supported yet; OCR could be added.
- Skills come from a fixed dictionary; a trained NER model or an LLM could find new skills.
- Future ideas: AI rewriting of resume bullet points, job recommendations, Hindi and regional-language resumes, a version for the university placement cell.

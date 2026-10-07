"""
NLP engine for the AI Resume Analyzer.

Pipeline (matches the project's five modules):
  M2  extract_text()      -> read text from the PDF
  M3  extract_skills()    -> find skills with spaCy's PhraseMatcher
  M4  text_similarity()   -> TF-IDF vectors + cosine similarity
      analyze()           -> combine into a match score
  M5  build_suggestions() -> tips shown on the dashboard
"""

import io
import re

import pdfplumber
import spacy
from spacy.matcher import PhraseMatcher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from skills import SKILLS

# Weight of each part in the final match score (must add up to 1).
TEXT_WEIGHT = 0.4
SKILL_WEIGHT = 0.6

# Short or everyday words that are only a skill when written in a specific
# case ("Go" the language vs "go" the verb, "REST" vs "the rest of").
AMBIGUOUS = {
    "c", "r", "go", "swift", "rust", "ruby", "dart", "express", "spring",
    "node", "rest", "mongo", "excel", "oracle", "ml", "dl", "ts", "js",
    "unix", "scrum",
}

# ---------------------------------------------------------------------------
# Skill matcher (built once when the module loads)
# ---------------------------------------------------------------------------
_nlp = spacy.blank("en")  # tokenizer only: fast, no model download needed
_match_any_case = PhraseMatcher(_nlp.vocab, attr="LOWER")
_match_exact_case = PhraseMatcher(_nlp.vocab, attr="ORTH")

for _name, _aliases in SKILLS.items():
    any_case, exact_case = [], []
    for term in [_name, *_aliases]:
        if term.lower() in AMBIGUOUS:
            variants = {term.upper(), term[0].upper() + term[1:]}
            if term != term.lower():
                variants.add(term)
            exact_case.extend(_nlp.make_doc(v) for v in variants)
        else:
            any_case.append(_nlp.make_doc(term))
    if any_case:
        _match_any_case.add(_name, any_case)
    if exact_case:
        _match_exact_case.add(_name, exact_case)


class ResumeReadError(Exception):
    """Raised when no text can be read from the uploaded PDF."""


# ---------------------------------------------------------------------------
# M2: text extraction
# ---------------------------------------------------------------------------
def extract_text(pdf_bytes: bytes) -> str:
    """Return all text from a PDF given as bytes. Nothing is written to disk."""
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
    except Exception as exc:  # corrupt or encrypted PDF
        raise ResumeReadError("This PDF could not be opened. It may be damaged or password-protected.") from exc

    text = "\n".join(pages).strip()
    if len(text) < 30:
        raise ResumeReadError(
            "No readable text was found in this PDF. It may be a scanned image; "
            "please upload a text-based PDF (for example, exported from Word or Google Docs)."
        )
    return text


def clean_text(text: str) -> str:
    """Lowercase and keep only letters, digits and the symbols used in skill names."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


# ---------------------------------------------------------------------------
# M3: skill extraction
# ---------------------------------------------------------------------------
def _skill_spans(text: str):
    """Return the tokenized text and a sorted list of (start, end, skill name)."""
    doc = _nlp.make_doc(text)
    spans = set()
    for matcher in (_match_any_case, _match_exact_case):
        for match_id, start, end in matcher(doc):
            spans.add((start, end, _nlp.vocab.strings[match_id]))
    return doc, sorted(spans)


def extract_skills(text: str) -> set:
    """Return the set of skill names found in the text."""
    _doc, spans = _skill_spans(text)
    return {name for _s, _e, name in spans}


def extract_requirements(job_text: str) -> list:
    """
    Group the job's skills into requirements. Skills joined by "or" / "/"
    (e.g. "Flask or Django") are alternatives: either one satisfies it.
    Returns a list of sets, one set per requirement.
    """
    doc, spans = _skill_spans(job_text)
    groups, prev_end = [], None
    for start, end, name in spans:
        joined = (
            prev_end is not None
            and 1 <= start - prev_end <= 2
            and all(doc[i].lower_ in {"or", "/"} for i in range(prev_end, start))
        )
        if joined:
            groups[-1].add(name)
        else:
            groups.append({name})
        prev_end = end

    unique = {frozenset(g) for g in groups}
    # A skill required on its own makes any "X or Y" group containing it redundant.
    return [set(g) for g in unique if not any(other < g for other in unique)]


# ---------------------------------------------------------------------------
# M4: TF-IDF + cosine similarity
# ---------------------------------------------------------------------------
def text_similarity(resume_text: str, job_text: str) -> float:
    """Cosine similarity (0 to 1) between the TF-IDF vectors of the two texts."""
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 1),
        token_pattern=r"(?u)\b[a-z0-9][a-z0-9+#]*",
    )
    try:
        vectors = vectorizer.fit_transform([clean_text(resume_text), clean_text(job_text)])
    except ValueError:  # both texts were only stop words
        return 0.0
    return float(cosine_similarity(vectors[0], vectors[1])[0][0])


def score_label(score: int) -> str:
    if score >= 75:
        return "Strong match"
    if score >= 50:
        return "Good match"
    if score >= 30:
        return "Fair match"
    return "Low match"


# ---------------------------------------------------------------------------
# M5: suggestions
# ---------------------------------------------------------------------------
SECTIONS = {
    "Education": r"\beducation\b|\bacademic",
    "Skills": r"\bskills?\b|technical skills",
    "Projects": r"\bprojects?\b",
    "Experience": r"\bexperience\b|\binternships?\b|\bwork history\b",
}


def build_suggestions(resume_text: str, missing: list, coverage: int, word_count: int) -> list:
    tips = []
    lower = resume_text.lower()

    if missing:
        tips.append(
            "Add these skills from the job description if you have them: "
            + ", ".join(missing[:6]) + "."
        )
    if missing and coverage < 50:
        tips.append("Your resume covers less than half of the skills this job asks for. Tailor it to this role.")

    for section, pattern in SECTIONS.items():
        if not re.search(pattern, lower):
            tips.append(f"Add a clear \"{section}\" section heading so ATS software can find it.")

    numbers = re.findall(r"\d+\s*%|\b\d+\+?\b", resume_text)
    if len(numbers) < 4:
        tips.append("Add numbers to show impact, for example \"improved page load time by 30%\".")

    if word_count < 200:
        tips.append(f"Your resume is short ({word_count} words). Add more detail about your projects and skills.")
    elif word_count > 1000:
        tips.append(f"Your resume is long ({word_count} words). Keep it to one or two pages.")

    if not re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", resume_text):
        tips.append("Add a professional email address at the top.")
    if "linkedin" not in lower and "github" not in lower:
        tips.append("Add your LinkedIn or GitHub profile link.")

    if not tips:
        tips.append("Great work! Your resume is well aligned with this job.")
    return tips


# ---------------------------------------------------------------------------
# Full analysis
# ---------------------------------------------------------------------------
def analyze(resume_text: str, job_text: str) -> dict:
    resume_skills = extract_skills(resume_text)
    requirements = extract_requirements(job_text)
    job_skills = set().union(*requirements) if requirements else set()

    met = [g for g in requirements if g & resume_skills]
    unmet = [g for g in requirements if not g & resume_skills]

    matched = sorted(job_skills & resume_skills)
    missing = sorted(" / ".join(sorted(g)) for g in unmet)
    extra = sorted(resume_skills - job_skills)

    similarity = round(text_similarity(resume_text, job_text) * 100)
    coverage = round(len(met) / len(requirements) * 100) if requirements else None

    if coverage is None:
        score = similarity
    else:
        score = round(TEXT_WEIGHT * similarity + SKILL_WEIGHT * coverage)

    word_count = len(resume_text.split())
    return {
        "score": score,
        "label": score_label(score),
        "text_similarity": similarity,
        "skill_coverage": coverage,
        "matched_skills": matched,
        "missing_skills": missing,
        "extra_skills": extra,
        "word_count": word_count,
        "suggestions": build_suggestions(resume_text, missing, coverage or 0, word_count),
    }

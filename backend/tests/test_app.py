"""
Automated tests. TC01-TC06 are the test cases shown in the project report and slides.
Run from the backend folder:  python -m pytest -v
"""

import io
import os
import sys

import pytest

BACKEND = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(BACKEND)
sys.path.insert(0, BACKEND)
sys.path.insert(0, os.path.join(ROOT, "samples"))

import make_samples  # noqa: E402
from analyzer import extract_skills, extract_text, text_similarity  # noqa: E402
from app import app  # noqa: E402

SAMPLES = os.path.join(ROOT, "samples")


@pytest.fixture(scope="session", autouse=True)
def sample_files():
    make_samples.main()


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    return app.test_client()


def read(name, mode="rb"):
    with open(os.path.join(SAMPLES, name), mode) as fh:
        return fh.read()


def post(client, file_bytes, filename, job_text):
    data = {"job_description": job_text}
    if file_bytes is not None:
        data["resume"] = (io.BytesIO(file_bytes), filename)
    return client.post("/api/analyze", data=data, content_type="multipart/form-data")


# ---------------- Test cases from the report ----------------

def test_tc01_valid_pdf_text_extracted():
    text = extract_text(read("sample_resume.pdf"))
    assert "Riya Verma" in text
    assert "Flask" in text


def test_tc02_jpg_rejected(client):
    fake_jpg = b"\xff\xd8\xff\xe0" + b"0" * 1000
    res = post(client, fake_jpg, "photo.jpg", read("job_description.txt", "r"))
    assert res.status_code == 400
    assert "Only PDF" in res.get_json()["error"]


def test_tc03_empty_job_description(client):
    res = post(client, read("sample_resume.pdf"), "resume.pdf", "   ")
    assert res.status_code == 400
    assert "job description" in res.get_json()["error"]


def test_tc04_matching_resume_scores_high(client):
    res = post(client, read("sample_resume.pdf"), "resume.pdf", read("job_description.txt", "r"))
    body = res.get_json()
    assert res.status_code == 200
    assert body["score"] >= 50
    assert "Python" in body["matched_skills"]
    assert "Docker" in body["missing_skills"]


def test_tc05_unrelated_resume_scores_low(client):
    good = post(client, read("sample_resume.pdf"), "a.pdf", read("job_description.txt", "r")).get_json()
    bad = post(client, read("unrelated_resume.pdf"), "b.pdf", read("job_description.txt", "r")).get_json()
    assert bad["score"] < 30
    assert bad["score"] < good["score"]


def test_tc06_file_over_5mb_rejected(client):
    big = b"%PDF-1.4\n" + b"0" * (5 * 1024 * 1024 + 10)
    res = post(client, big, "big.pdf", read("job_description.txt", "r"))
    assert res.status_code == 413
    assert "too large" in res.get_json()["error"]


# ---------------- Extra unit tests ----------------

def test_missing_file(client):
    res = post(client, None, "", read("job_description.txt", "r"))
    assert res.status_code == 400


def test_fake_pdf_extension_rejected(client):
    res = post(client, b"just some text", "resume.pdf", read("job_description.txt", "r"))
    assert res.status_code == 400


def test_skill_aliases_and_case():
    skills = extract_skills("Worked with ReactJS, node js, Golang and C++ in an Agile team.")
    assert {"React", "Node.js", "Go", "C++", "Agile"} <= skills


def test_everyday_words_are_not_skills():
    skills = extract_skills("I will go to the rest of the meetings and excel at teamwork.")
    assert "Go" not in skills
    assert "REST API" not in skills
    assert "Excel" not in skills
    assert "Teamwork" in skills


def test_or_alternatives_count_as_one_requirement():
    from analyzer import analyze
    result = analyze(
        "Python developer skilled in Flask and MySQL. " * 3,
        "We need Python, Flask or Django, and MySQL or PostgreSQL experience.",
    )
    assert result["skill_coverage"] == 100
    assert result["missing_skills"] == []


def test_similarity_range():
    same = text_similarity("python flask sql developer", "python flask sql developer")
    different = text_similarity("python flask sql developer", "hotel guest housekeeping")
    assert same == pytest.approx(1.0)
    assert different == pytest.approx(0.0)


def test_health(client):
    assert client.get("/api/health").get_json() == {"status": "ok"}

"""
Creates sample files for demos and tests:
  sample_resume.pdf     - a fictional BCA student resume (good match for the job)
  unrelated_resume.pdf  - a fictional hotel-management resume (poor match)
  job_description.txt   - a Junior Python Developer job description

Run:  python samples/make_samples.py
"""

import os

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

HERE = os.path.dirname(os.path.abspath(__file__))

GOOD_RESUME = """Riya Verma
riya.verma@example.com | github.com/riyaverma | linkedin.com/in/riyaverma

SUMMARY
Final-year BCA student and aspiring Python developer who enjoys building web apps
with clean backend code. Looking for a fresher role in backend or full-stack development.

EDUCATION
Bachelor of Computer Applications (BCA), 2022 - 2025, CGPA 8.4

TECHNICAL SKILLS
Python, Flask, SQL, MySQL, HTML, CSS, JavaScript, React, Git, GitHub, REST API, Data Structures

PROJECTS
Library Management System - Built a Flask web app with a MySQL database for 500+ books.
Created REST API endpoints for issuing and returning books and reduced manual work by 40%.
Expense Tracker - React frontend with a Python Flask backend; 3 charts for monthly spending.
Weather Dashboard - JavaScript app using a public REST API, deployed on GitHub Pages.

EXPERIENCE
Web Development Intern, local startup, 2 months - built 6 responsive pages with HTML, CSS and React.
Wrote SQL queries for reports and fixed 15+ bugs in the Python backend.

ACHIEVEMENTS
Solved 200+ problems on data structures and algorithms. Team lead for a college hackathon.
"""

UNRELATED_RESUME = """Arjun Mehta
arjun.mehta@example.com

EDUCATION
Bachelor of Hotel Management, 2021 - 2024

SKILLS
Front office operations, guest relations, housekeeping supervision, food and beverage service,
event coordination, menu planning, inventory of linen and supplies.

EXPERIENCE
Front Desk Associate, city hotel, 1 year - handled check-in and check-out for 120 rooms.
Banquet Trainee - coordinated wedding and conference events for up to 300 guests.

ACHIEVEMENTS
Best trainee award for guest satisfaction. Fluent in Hindi, English and Punjabi.
"""

JOB_DESCRIPTION = """Junior Python Developer (Fresher)

We are looking for a Junior Python Developer to join our product team.

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
- Good communication and teamwork skills.
"""


def write_pdf(path: str, text: str) -> None:
    pdf = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    y = height - 60
    for line in text.splitlines():
        if line.isupper() and line.strip():
            pdf.setFont("Helvetica-Bold", 12)
            y -= 6
        else:
            pdf.setFont("Helvetica", 10)
        pdf.drawString(50, y, line)
        y -= 16
    pdf.save()


def main() -> None:
    write_pdf(os.path.join(HERE, "sample_resume.pdf"), GOOD_RESUME)
    write_pdf(os.path.join(HERE, "unrelated_resume.pdf"), UNRELATED_RESUME)
    with open(os.path.join(HERE, "job_description.txt"), "w", encoding="utf-8") as fh:
        fh.write(JOB_DESCRIPTION)
    print("Sample files written to", HERE)


if __name__ == "__main__":
    main()

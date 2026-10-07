# Viva preparation: likely questions and answers

Answer in your own words. Short, clear answers are best.

## About the project

**1. What does your project do?**
It compares a resume with a job description and shows a match score, the skills that match, the skills that are missing, and tips to improve. It helps students get past ATS filters.

**2. What is an ATS?**
An Applicant Tracking System. Companies use it to automatically filter resumes, mostly by keywords, before a recruiter reads them.

**3. Why did you choose this project?**
Many students get rejected without feedback. This tool shows them exactly what is missing, for free.

## The AI / NLP part

**4. What is TF-IDF?**
Term Frequency × Inverse Document Frequency. It turns text into numbers. A word gets a high weight if it appears often in one document but rarely in others, so important words like "Flask" count more than common words like "the".

**5. What is cosine similarity?**
It measures the angle between two vectors: cos θ = (A · B) / (‖A‖ ‖B‖). Same direction gives 1 (identical), unrelated gives 0. It ignores document length, which is why it suits comparing a long resume with a short job post.

**6. How is the final score calculated?**
60% skill coverage + 40% text similarity. Skill coverage is the share of the job's required skills found in the resume. Skills get more weight because recruiters filter on them.

**7. Why not just count matching keywords?**
Simple counting treats every word equally and is affected by length. TF-IDF gives important words more weight, and cosine similarity is not affected by document length. I combine it with skill matching for accuracy.

**8. How do you find skills?**
With spaCy's PhraseMatcher and a dictionary of about 100 skills with aliases, so "ReactJS" and "React.js" both count as React. Short words like "Go" or "REST" only count when written in the proper case, so "go to the rest of" is not a false match.

**9. What if the job says "Flask or Django"?**
The program detects "or" between two skills and treats them as one requirement: having either one is enough.

**10. Is this machine learning?**
It uses NLP techniques from machine learning libraries (scikit-learn, spaCy). It is not a trained model; it is an information-retrieval approach, which needs no training data and is easy to explain. A trained model is part of future scope.

## Technical

**11. Why Flask and React?**
Flask is lightweight and Python has the best NLP libraries. React builds a fast, component-based interface.

**12. What is a REST API? Which endpoints do you have?**
A way for the frontend and backend to talk over HTTP using JSON. I have GET /api/health and POST /api/analyze.

**13. How does the frontend send the file?**
As multipart/form-data using the fetch API with a FormData object.

**14. How do you keep user data private?**
Files are processed in memory and never saved to disk or a database.

**15. What validation do you do?**
Only PDFs are allowed (checked by extension and the %PDF file header), a maximum of 5 MB, and the job description is required. The frontend checks first, and the backend checks again.

**16. What happens with a scanned PDF?**
There is no text layer, so the app shows a clear error asking for a text-based PDF. OCR is future scope.

**17. How did you test it?**
13 automated tests with pytest, including the six test cases TC01–TC06: positive tests (valid resume, good match) and negative tests (wrong file type, empty field, file too large).

**18. Which SDLC model did you follow?**
Agile, in five sprints: requirements, design, backend + AI, frontend, testing + deployment. Agile let me change requirements after each sprint.

## General

**19. What was the biggest challenge?**
False skill matches, for example "go" the verb being read as the Go language, and "Flask or Django" counting as two requirements. I fixed both with case-sensitive matching for short words and "or" detection.

**20. What would you improve?**
OCR for scanned PDFs, an LLM to rewrite resume bullets, job recommendations, more languages, and a version for the placement cell.

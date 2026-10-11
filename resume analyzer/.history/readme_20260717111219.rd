# Resume Analyzer (Flask + TF-IDF + Skill Matching)

A web app that compares an uploaded resume against a job description and reports
a match score plus a skill-gap breakdown — fully offline, no API key needed.

## Features
- Upload resume as PDF, DOCX, or TXT
- Paste any job description
- Overall match score (blend of text similarity + skill coverage)
- Matched skills, missing skills, and extra skills on your resume
- Drag-and-drop file upload
- Clean, responsive dark-mode UI

## Project Structure
```
resume-analyzer/
├── app.py                 # Flask backend + analysis logic
├── skills_data.py         # Predefined technical + soft skills list
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html         # Main page
└── static/
    ├── style.css           # Styling
    └── script.js           # Frontend logic (fetch calls, UI updates)
```

## Setup & Run

1. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**
   ```bash
   python app.py
   ```

4. **Open your browser**
   ```
   http://127.0.0.1:5000
   ```

## How it works
1. **Text extraction** — `pdfplumber` reads PDFs, `python-docx` reads Word files, plain `.txt` is read directly.
2. **Skill matching** — the resume and job description are scanned against a predefined list of ~100 technical and soft skills (`skills_data.py`) using word-boundary-safe matching, so "React" matches but "reaction" doesn't.
3. **Overall similarity** — `scikit-learn`'s `TfidfVectorizer` + cosine similarity measures how closely the overall wording of the resume matches the job description.
4. **Final score** — a weighted blend: 60% skill coverage (how many of the JD's required skills appear on the resume) + 40% text similarity.

## Customizing the skill list
Edit `skills_data.py` to add skills relevant to your target roles (e.g. add
domain-specific tools, certifications, or frameworks). The matcher automatically
picks up any new entries — no other code changes needed.

## Notes
- Works best on resumes with selectable text (not scanned images — those need OCR, which isn't included here).
- To deploy publicly, use a production server (e.g. `gunicorn app:app`) instead of Flask's built-in dev server.

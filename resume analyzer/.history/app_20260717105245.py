"""
AI Resume Analyzer - Flask Backend
------------------------------------
Matches an uploaded resume (PDF / DOCX / TXT) against a pasted job
description. Produces an overall match score (TF-IDF cosine similarity)
plus a skill-gap breakdown (matched vs missing skills).

Fully offline - no API key required.
"""

import re
import io

from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import pdfplumber
import docx

from skills_data import ALL_SKILLS

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB upload limit


# ---------------------------------------------------------
# Text extraction helpers
# ---------------------------------------------------------
def extract_text_from_pdf(file_stream) -> str:
    text_parts = []
    with pdfplumber.open(file_stream) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)


def extract_text_from_docx(file_stream) -> str:
    document = docx.Document(file_stream)
    return "\n".join(p.text for p in document.paragraphs)


def extract_text(file) -> str:
    filename = file.filename.lower()
    stream = io.BytesIO(file.read())

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(stream)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(stream)
    elif filename.endswith(".txt"):
        return stream.read().decode("utf-8", errors="ignore")
    else:
        raise ValueError("Unsupported file type. Please upload a PDF, DOCX, or TXT file.")


# ---------------------------------------------------------
# Analysis logic
# ---------------------------------------------------------
def find_skills(text: str) -> set:
    text_lower = text.lower()
    found = set()
    for skill in ALL_SKILLS:
        # word-boundary-safe match, handles multi-word skills like "machine learning"
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
        if re.search(pattern, text_lower):
            found.add(skill)
    return found


def compute_similarity(resume_text: str, jd_text: str) -> float:
    if not resume_text.strip() or not jd_text.strip():
        return 0.0
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(score * 100, 1)


def analyze(resume_text: str, jd_text: str) -> dict:
    resume_skills = find_skills(resume_text)
    jd_skills = find_skills(jd_text)

    matched = sorted(resume_skills & jd_skills)
    missing = sorted(jd_skills - resume_skills)
    extra = sorted(resume_skills - jd_skills)

    similarity_score = compute_similarity(resume_text, jd_text)

    skill_coverage = (
        round(len(matched) / len(jd_skills) * 100, 1) if jd_skills else 0.0
    )

    # Blend overall text similarity with skill coverage for a final score
    final_score = round((similarity_score * 0.4) + (skill_coverage * 0.6), 1)

    return {
        "final_score": final_score,
        "similarity_score": similarity_score,
        "skill_coverage": skill_coverage,
        "matched_skills": matched,
        "missing_skills": missing,
        "extra_skills": extra,
        "jd_skill_count": len(jd_skills),
        "resume_skill_count": len(resume_skills),
    }


# ---------------------------------------------------------
# Routes
# ---------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze_route():
    jd_text = request.form.get("job_description", "").strip()

    if not jd_text:
        return jsonify({"error": "Please paste a job description."}), 400

    if len(jd_text.split()) < 10:
        return jsonify({"error": "Job description seems too short. Please paste the full listing."}), 400

    resume_file = request.files.get("resume_file")
    if not resume_file or resume_file.filename == "":
        return jsonify({"error": "Please upload a resume file (PDF, DOCX, or TXT)."}), 400

    try:
        resume_text = extract_text(resume_file)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "Could not read the resume file. Make sure it isn't corrupted or scanned as an image."}), 400

    if len(resume_text.split()) < 20:
        return jsonify({"error": "Couldn't extract enough text from the resume. If it's a scanned/image PDF, try a text-based version."}), 400

    try:
        result = analyze(resume_text, jd_text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

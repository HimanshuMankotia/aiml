import streamlit as st

from src.pdf_parser import extract_text_from_pdf
from src.preprocess import preprocess_text
from src.skill_extractor import extract_skills
from src.similarity import calculate_match_percentage
from src.similarity import skill_match_score
from src.similarity import final_score


st.set_page_config(page_title="AI Resume Screener", layout="wide")

st.title("🤖 AI Resume Screening System")

st.write("Upload resumes and compare them with a Job Description using NLP.")


job_description = st.text_area("📄 Paste Job Description")


uploaded_files = st.file_uploader(
    "📂 Upload Resumes (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)


if st.button("🚀 Analyze Resumes"):

    if job_description == "":
        st.warning("Please paste a Job Description")

    elif uploaded_files is None or len(uploaded_files) == 0:
        st.warning("Please upload at least one resume")

    else:

        st.subheader("📊 Analysis Results")

        jd_processed = preprocess_text(job_description)

        jd_skills = extract_skills(jd_processed)

        results = []

        for uploaded_file in uploaded_files:

            resume_text = extract_text_from_pdf(uploaded_file)

            resume_text = preprocess_text(resume_text)

            resume_skills = extract_skills(resume_text)

            similarity_score = calculate_match_percentage(
                resume_text,
                jd_processed
            )

            skill_score = skill_match_score(
                resume_skills,
                jd_skills
            )

            final_score_value = final_score(
                similarity_score,
                skill_score
            )

            results.append((uploaded_file.name, final_score_value))

            st.write("--------------------------------------------------")

            st.write(f"📄 Resume: {uploaded_file.name}")

            st.write(f"🎯 Final AI Match Score: {round(final_score_value,2)}%")

            matched_skills = list(
                set(resume_skills).intersection(set(jd_skills))
            )

            st.write("✅ Skills Matched:", matched_skills)

        results.sort(key=lambda x: x[1], reverse=True)

        st.subheader("🏆 Candidate Ranking")

        for i, (name, score) in enumerate(results):

            st.write(f"{i+1}. {name} — {round(score,2)}%")

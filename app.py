import streamlit as st
from src.pdf_parser import extract_text_from_pdf
from src.preprocess import preprocess_text
from src.skill_extractor import extract_skills
from src.similarity import calculate_match_percentage, skill_match_score

st.set_page_config(page_title="AI Resume Screener", layout="wide")

st.markdown(
"""
<h1 style='text-align: center;'>🤖 AI Resume Screening System</h1>
<p style='text-align: center; font-size:18px;'>
Upload resumes and compare them with a Job Description using NLP & AI scoring.
</p>
""",
unsafe_allow_html=True
)

st.sidebar.header("📄 Job Description")
job_description = st.sidebar.text_area(
"Paste Job Description",
height=250
)

st.sidebar.markdown("---")
st.sidebar.info("Upload multiple resumes and click Analyze to rank candidates.")

uploaded_files = st.file_uploader(
"📂 Upload Resumes (PDF)",
type=["pdf"],
accept_multiple_files=True
)

if st.button("🚀 Analyze Resumes"):

    if job_description == "":
        st.warning("Please paste a Job Description first.")
    
    elif uploaded_files is None or len(uploaded_files) == 0:
        st.warning("Please upload at least one resume.")
    
    else:

        st.subheader("📊 Analysis Results")

        jd_processed = preprocess_text(job_description)
        jd_skills = extract_skills(jd_processed)

        results = []

        for uploaded_file in uploaded_files:

            resume_text = extract_text_from_pdf(uploaded_file)
            resume_text = preprocess_text(resume_text)

            resume_skills = extract_skills(resume_text)

            similarity_score = calculate_match_percentage(resume_text, jd_processed)
            skill_score = skill_match_score(resume_skills, jd_skills)

            final_score = round((0.7 * similarity_score) + (0.3 * skill_score * 100), 2)

            results.append((uploaded_file.name, final_score))

            matched_skills = list(set(resume_skills).intersection(set(jd_skills)))

            col1, col2 = st.columns([3,1])

            with col1:
                st.markdown(f"### 📄 {uploaded_file.name}")

                if final_score >= 70:
                    color = "green"
                elif final_score >= 40:
                    color = "orange"
                else:
                    color = "red"

                st.progress(int(final_score))

                st.markdown(
                    f"<span style='font-size:18px;'>🎯 Match Score: "
                    f"<b style='color:{color};'>{final_score}%</b></span>",
                    unsafe_allow_html=True
                )

                if matched_skills:
                    badges = " ".join([f"`{skill}`" for skill in matched_skills])
                    st.markdown(f"**✅ Skills Matched:** {badges}")
                else:
                    st.markdown("❌ No major skills matched")

            st.markdown("---")

        results.sort(key=lambda x: x[1], reverse=True)

        st.subheader("🏆 Candidate Ranking")

        for i, (name, score) in enumerate(results):

            if score >= 70:
                medal = "🥇"
            elif score >= 50:
                medal = "🥈"
            else:
                medal = "🥉"

            st.write(f"{medal} **{name} — {score}%**")
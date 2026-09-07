"""
Presentation Layer (Streamlit UI).
Responsibility: Render user interface, manage state, and orchestrate application components.
"""

import os
import streamlit as st
from dotenv import load_dotenv

from analyzer import ResumeAnalyzerService, analyze_resume
from resume_parser import ResumeParser, extract_resume_text

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

def initialize_ui():
    st.title("📄 AI Resume Analyzer & ATS Matcher")
    st.markdown("Upload your resume and paste a target job description to analyze ATS compatibility, identify skill gaps, and get actionable suggestions.")

def sidebar_configuration():
    st.sidebar.header("🔑 Configuration")
    env_key = os.getenv("GROQ_API_KEY", "")
    
    if env_key:
        api_key = env_key
        st.sidebar.success("Groq API key detected from environment.")
    else:
        api_key = st.sidebar.text_input("Groq API Key", type="password", help="Enter your Groq API key here.")
        
    return api_key

def main():
    initialize_ui()
    api_key = sidebar_configuration()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Upload Resume")
        uploaded_file = st.file_uploader("Upload PDF or DOCX document", type=["pdf", "docx"])

    with col2:
        st.subheader("2. Job Description")
        job_description = st.text_area("Paste job requirements here...", height=220)

    if st.button("🚀 Analyze Compatibility", type="primary", use_container_width=True):
        if not api_key:
            st.error("Please provide a valid Groq API key in the sidebar or environment.")
            return

        if not uploaded_file:
            st.warning("Please upload a resume file (PDF or DOCX).")
            return

        if not job_description.strip():
            st.warning("Please paste a job description.")
            return

        try:
            with st.spinner("Processing document and running analysis..."):
                file_bytes = uploaded_file.read()
                resume_text = extract_resume_text(file_bytes, uploaded_file.name)

                results = analyze_resume(resume_text, job_description, api_key=api_key)

            # Display Results
            st.divider()
            st.header("📊 Analysis Dashboard")

            # Score Display
            score = results["match_score"]
            c1, c2 = st.columns([1, 3])
            with c1:
                st.metric("Match Score", f"{score}%")
            with c2:
                st.progress(score / 100)
                st.write(f"**Verdict:** {results['final_verdict']}")

            st.divider()

            # Skills Overview
            sk_col1, sk_col2 = st.columns(2)
            with sk_col1:
                st.subheader("✅ Matching Skills")
                if results["matching_skills"]:
                    for skill in results["matching_skills"]:
                        st.markdown(f"- {skill}")
                else:
                    st.write("None detected.")

            with sk_col2:
                st.subheader("❌ Missing Skills")
                if results["missing_skills"]:
                    for skill in results["missing_skills"]:
                        st.markdown(f"- {skill}")
                else:
                    st.write("None detected.")

            st.divider()

            # Keywords & Issues
            kw_col, prob_col = st.columns(2)
            with kw_col:
                st.subheader("🔑 Recommended ATS Keywords")
                if results["ats_keywords"]:
                    st.write(", ".join([f"`{kw}`" for kw in results["ats_keywords"]]))
                else:
                    st.write("None suggested.")

            with prob_col:
                st.subheader("⚠️ Resume Weaknesses")
                if results["resume_problems"]:
                    for prob in results["resume_problems"]:
                        st.markdown(f"- {prob}")
                else:
                    st.write("No critical weaknesses found.")

            st.divider()

            # Actionable Recommendations
            st.subheader("💡 Actionable Recommendations")
            for idx, rec in enumerate(results["recommendations"], 1):
                st.markdown(f"**{idx}.** {rec}")

        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")

if __name__ == "__main__":
    main()

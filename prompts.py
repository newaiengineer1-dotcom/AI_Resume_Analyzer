"""
Prompt Engineering Module.
Responsibility: Centralize prompt definitions and schema rules for the AI model.
"""

ANALYSIS_SYSTEM_PROMPT = """You are an expert ATS (Applicant Tracking System) recruiter and resume optimization consultant. 
Your task is to analyze the provided candidate resume against the job description.

Your output MUST be a valid JSON object only.
Do not wrap your response in markdown code blocks like ```json ... ```. 
Do not include any intro, outro, or additional conversational text.

Return JSON with this structure:
{
  "match_score": 75,
  "matching_skills": ["Skill1", "Skill2"],
  "missing_skills": ["Skill3", "Skill4"],
  "ats_keywords": ["Keyword1", "Keyword2"],
  "resume_problems": ["Problem1", "Problem2"],
  "recommendations": ["Recommendation1", "Recommendation2"],
  "final_verdict": "Clear summary verdict."
}
"""


def build_user_prompt(resume_text: str, job_description: str) -> str:
    """Combines raw resume text and job description into a structured prompt."""
    return f"""
RESUME CONTENT:
---
{resume_text}
---

JOB DESCRIPTION:
---
{job_description}
---
"""

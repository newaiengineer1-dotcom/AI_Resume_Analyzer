"""
AI Analysis Service Module.
Responsibility: Communicate with the Groq API and parse response schemas.
"""

import json
import os
from typing import Any, Dict
from groq import Groq
from pydantic import BaseModel, Field

from prompts import ANALYSIS_SYSTEM_PROMPT, build_user_prompt


class AnalysisResult(BaseModel):
    """Pydantic schema model for validating AI response integrity."""
    match_score: int = Field(ge=0, le=100)
    matching_skills: list[str]
    missing_skills: list[str]
    ats_keywords: list[str]
    resume_problems: list[str]
    recommendations: list[str]
    final_verdict: str


class ResumeAnalyzerService:
    """Manages AI-driven comparison between resumes and job descriptions."""

    def __init__(self, api_key: str | None = None, model_name: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Groq API key missing. Pass it or set the GROQ_API_KEY environment variable.")
        self.client = Groq(api_key=self.api_key)
        self.model_name = model_name

    def analyze(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """Sends resume and job description to Groq API and returns structured JSON analysis."""
        user_prompt = build_user_prompt(resume_text, job_description)

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": ANALYSIS_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("Received an empty response from Groq API.")

        raw_data = json.loads(content)
        validated_result = AnalysisResult(**raw_data)
        return validated_result.model_dump()


def analyze_resume(resume_text: str, job_description: str, api_key: str | None = None) -> Dict[str, Any]:
    """Convenience functional wrapper for backwards compatibility."""
    service = ResumeAnalyzerService(api_key=api_key)
    return service.analyze(resume_text, job_description)

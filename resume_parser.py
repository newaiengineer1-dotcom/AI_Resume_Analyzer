"""
Document Processing Module.
Responsibility: Handle text extraction from PDF and DOCX file inputs.
"""

import io
from docx import Document
from pypdf import PdfReader


class ResumeParser:
    """Extracts text content from binary document streams."""

    @staticmethod
    def extract_text(file_bytes: bytes, filename: str) -> str:
        """Determines file format and extracts readable text."""
        extension = filename.lower().split(".")[-1]
        
        if extension == "pdf":
            return ResumeParser._extract_from_pdf(file_bytes)
        elif extension == "docx":
            return ResumeParser._extract_from_docx(file_bytes)
        else:
            raise ValueError(f"Unsupported file format: .{extension}. Please upload a PDF or DOCX file.")

    @staticmethod
    def _extract_from_pdf(file_bytes: bytes) -> str:
        """Extracts text from PDF bytes."""
        reader = PdfReader(io.BytesIO(file_bytes))
        extracted_text = []
        
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text.append(text)
                
        full_text = "\n".join(extracted_text).strip()
        if not full_text:
            raise ValueError("Could not extract readable text from PDF. Ensure it is not a scanned image.")
        return full_text

    @staticmethod
    def _extract_from_docx(file_bytes: bytes) -> str:
        """Extracts text from DOCX bytes."""
        doc = Document(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        full_text = "\n".join(paragraphs).strip()
        
        if not full_text:
            raise ValueError("The provided DOCX document appears to be empty.")
        return full_text


def extract_resume_text(file_bytes: bytes, filename: str) -> str:
    """Convenience functional wrapper for backwards compatibility."""
    return ResumeParser.extract_text(file_bytes, filename)

# AI Resume Analyzer & ATS Matcher

A modular application built with Python, Streamlit, and Groq API to evaluate resume compatibility against job descriptions.

## Setup Instructions

### 1. Prerequisites
- Python 3.10+
- Groq API Key

### 2. Environment Setup
Clone the repository and set up a virtual environment:

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. API Key Setup
Create a `.env` file in the root directory:
```bash
cp .env.example .env
```
Edit `.env` and set your key:
```env
GROQ_API_KEY=your_actual_groq_api_key
```

## Running the Application
Launch the Streamlit app:
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

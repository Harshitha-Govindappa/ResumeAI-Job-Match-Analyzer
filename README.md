
# ResumeAI – AI-Powered Resume Analysis & Job Matching

ResumeAI is a Python-based web application built using Streamlit. It analyzes PDF resumes, compares them with job descriptions, identifies matching and missing skills, recommends suitable job roles, and provides learning suggestions.

## Features

- Upload resumes in PDF format
- Extract resume text using PyPDF
- Automatically identify technical skills
- Compare resumes with job descriptions
- Calculate text similarity using TF-IDF and Cosine Similarity
- Display matching and missing skills
- Calculate skill match percentage
- Recommend suitable job roles
- Provide learning suggestions for missing skills
- Store analysis history using SQLite
- Download resume analysis reports
- Interactive dashboard with Plotly charts

## Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- TF-IDF
- Cosine Similarity
- Plotly
- SQLite
- PyPDF

## Project Structure

```text
ResumeAI-Job-Match-Analyzer/
│
├── app.py
├── database.py
├── resume_parser.py
├── skills_analyzer.py
├── job_matcher.py
├── job_recommender.py
├── resume_suggestions.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
```

### 2. Open the project folder

```bash
cd ResumeAI-Job-Match-Analyzer
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment (Windows PowerShell)

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run app.py
```

## How to Use

1. Open the ResumeAI application.
2. Upload your resume in PDF format.
3. Enter the job description.
4. Click the Analyze Resume button.
5. View the similarity score and skill match percentage.
6. Check matching and missing skills.
7. Explore recommended job roles.
8. Review learning suggestions.
9. Download the analysis report.

## How It Works

1. PyPDF extracts text from the uploaded resume.
2. Python keyword matching identifies skills.
3. TF-IDF and Cosine Similarity compare resume text with the job description.
4. Predefined skill requirements are used to recommend job roles.
5. Learning suggestions are generated for missing skills.
6. SQLite stores the analysis history.

## Limitations

- Skill detection uses a predefined keyword list.
- Job recommendations are based on predefined skill requirements.
- Similarity percentage is a text similarity measure, not an official ATS score.
- The application does not predict hiring decisions.

## Author

Harshitha G

B.E. Information Science and Engineering

GitHub: https://github.com/Harshitha-Govindappa

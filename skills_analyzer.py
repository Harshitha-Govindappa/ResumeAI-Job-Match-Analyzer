
import re

# Skills supported by ResumeAI
SKILLS = [
    "Python",
    "SQL",
    "MySQL",
    "Power BI",
    "Excel",
    "Machine Learning",
    "Deep Learning",
    "Pandas",
    "NumPy",
    "Matplotlib",
    "Scikit-learn",
    "Java",
    "Tableau",
    "Statistics",
    "Data Analysis",
    "Data Visualization",
    "Data Cleaning",
    "EDA"
]


def extract_skills(resume_text):

    found_skills = []

    text = resume_text.lower()

    for skill in SKILLS:

        # Match complete skill names
        pattern = r"(?<!\w)" + re.escape(
            skill.lower()
        ) + r"(?!\w)"

        if re.search(pattern, text):

            found_skills.append(skill)

    return found_skills

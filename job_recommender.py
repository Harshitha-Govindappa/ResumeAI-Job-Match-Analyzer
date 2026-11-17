
job_roles = {
    "Data Analyst": [
        "Python", "SQL", "MySQL", "Excel", "Power BI",
        "Pandas", "NumPy", "Statistics",
        "Data Analysis", "Data Cleaning", "EDA",
        "Data Visualization"
    ],

    "Data Scientist": [
        "Python", "SQL", "Machine Learning",
        "Deep Learning", "Pandas", "NumPy",
        "Statistics", "Scikit-learn"
    ],

    "Business Analyst": [
        "SQL", "MySQL", "Excel", "Power BI",
        "Data Analysis", "Data Visualization",
        "Statistics", "EDA"
    ],

    "Python Developer": [
        "Python", "SQL", "Java"
    ],

    "Machine Learning Engineer": [
        "Python", "Machine Learning", "Deep Learning",
        "NumPy", "Pandas", "Scikit-learn"
    ]
}


def recommend_jobs(resume_skills):
    recommendations = []

    for role, required_skills in job_roles.items():

        matched = [
            skill for skill in required_skills
            if skill in resume_skills
        ]

        missing = [
            skill for skill in required_skills
            if skill not in resume_skills
        ]

        score = round(
            (len(matched) / len(required_skills)) * 100, 2
        )

        recommendations.append({
            "Job Role": role,
            "Match Percentage": score,
            "Matching Skills": matched,
            "Missing Skills": missing
        })

    recommendations.sort(
        key=lambda x: x["Match Percentage"],
        reverse=True
    )

    return recommendations

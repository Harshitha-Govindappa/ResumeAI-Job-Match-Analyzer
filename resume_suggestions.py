
skill_suggestions = {
    "Statistics": [
        "Learn Mean, Median and Mode",
        "Understand Probability",
        "Practice Standard Deviation and Variance",
        "Learn Correlation and Hypothesis Testing"
    ],
    "Deep Learning": [
        "Understand Neural Networks",
        "Learn TensorFlow or PyTorch basics",
        "Practice basic Deep Learning projects"
    ],
    "Machine Learning": [
        "Learn Regression and Classification",
        "Understand Train-Test Split",
        "Practice model evaluation"
    ],
    "Scikit-learn": [
        "Learn model training using Scikit-learn",
        "Practice preprocessing and model evaluation"
    ],
    "Java": [
        "Learn Java fundamentals",
        "Practice OOP concepts"
    ]
}


def generate_suggestions(missing_skills):
    suggestions = {}

    for skill in missing_skills:
        if skill in skill_suggestions:
            suggestions[skill] = skill_suggestions[skill]
        else:
            suggestions[skill] = [
                f"Learn the fundamentals of {skill}",
                f"Practice {skill} with a small project"
            ]

    return suggestions

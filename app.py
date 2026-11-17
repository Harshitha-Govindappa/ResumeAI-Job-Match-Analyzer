
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from database import (
    create_table,
    save_analysis,
    get_analysis_history
)

from resume_parser import extract_resume_text
from skills_analyzer import extract_skills
from job_matcher import calculate_match
from job_recommender import recommend_jobs
from resume_suggestions import generate_suggestions


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="ResumeAI | Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

create_table()


# ==========================================
# 2. PROFESSIONAL CSS DESIGN
# ==========================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #F5F7FB;
}

/* Main content spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Main title */
.main-title {
    font-size: 40px;
    font-weight: 800;
    color: #1E3A8A;
    letter-spacing: -1px;
    margin-bottom: 0px;
}

/* Subtitle */
.sub-title {
    font-size: 16px;
    color: #64748B;
    margin-top: 5px;
}

/* Section headings */
h1, h2, h3 {
    color: #1E293B;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

/* Buttons */
.stButton > button {
    background-color: #2563EB;
    color: white;
    border-radius: 9px;
    border: none;
    padding: 10px 20px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #1D4ED8;
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #EFF4FF;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background-color: white;
    border-radius: 12px;
    padding: 12px;
}

/* Text area */
.stTextArea textarea {
    border-radius: 10px;
    background-color: white;
}

/* Divider */
hr {
    border-color: #DCE3EF;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. PROFESSIONAL HEADER
# ==========================================

col1, col2 = st.columns([3, 1])

with col1:

    st.markdown(
        '<p class="main-title">📄 ResumeAI</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="sub-title">'
        'AI-Powered Resume Analysis & Job Matching'
        '</p>',
        unsafe_allow_html=True
    )

with col2:

    st.info("🚀 Portfolio Project")

st.divider()


# ==========================================
# 4. SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("📄 ResumeAI")

st.sidebar.caption("Smart Resume Analysis Platform")

page = st.sidebar.radio(
    "Navigation",
    [
        "Resume Analyzer",
        "Analysis History",
        "About Project"
    ]
)

st.sidebar.divider()

st.sidebar.markdown("### Features")

st.sidebar.write("📄 Resume PDF Upload")
st.sidebar.write("📊 Similarity Analysis")
st.sidebar.write("🎯 Skills Matching")
st.sidebar.write("💼 Job Recommendations")
st.sidebar.write("📚 Learning Suggestions")
st.sidebar.write("🗄️ SQLite Database")


# ==========================================
# 5. RESUME ANALYZER PAGE
# ==========================================

if page == "Resume Analyzer":

    st.header("Resume Analysis")

    st.write(
        "Upload your resume and enter a job description "
        "to analyze your skills and discover suitable job roles."
    )

    col1, col2 = st.columns([1, 1])

    with col1:

        uploaded_file = st.file_uploader(
            "Upload your Resume (PDF)",
            type=["pdf"]
        )

    with col2:

        st.info(
            "Supported format: PDF\n\n"
            "Upload a text-based PDF for best results."
        )

    job_description = st.text_area(
        "Enter Job Description",
        placeholder="Paste the complete job description here...",
        height=220
    )

    analyze_button = st.button(
        "🔍 Analyze Resume",
        type="primary",
        use_container_width=True
    )

    # ======================================
    # 6. ANALYZE RESUME
    # ======================================

    if analyze_button:

        if uploaded_file is None:

            st.error("Please upload your resume PDF.")

        elif not job_description.strip():

            st.error("Please enter a job description.")

        else:

            try:

                with st.spinner("Analyzing your resume..."):

                    # Extract resume text
                    uploaded_file.seek(0)

                    resume_text = extract_resume_text(
                        uploaded_file
                    )

                    if not resume_text.strip():

                        st.error(
                            "No readable text found in this PDF. "
                            "Please upload a text-based PDF."
                        )

                    else:

                        # Extract skills
                        resume_skills = extract_skills(
                            resume_text
                        )

                        job_skills = extract_skills(
                            job_description
                        )

                        # Matching skills
                        matched_skills = [
                            skill for skill in job_skills
                            if skill in resume_skills
                        ]

                        # Missing skills
                        missing_skills = [
                            skill for skill in job_skills
                            if skill not in resume_skills
                        ]

                        # Skill percentage
                        if job_skills:

                            skill_score = round(
                                len(matched_skills)
                                / len(job_skills) * 100,
                                2
                            )

                        else:

                            skill_score = 0

                        # Text similarity
                        similarity_score = calculate_match(
                            resume_text,
                            job_description
                        )

                        # Save database record
                        save_analysis(
                            uploaded_file.name,
                            job_description,
                            similarity_score,
                            skill_score,
                            matched_skills,
                            missing_skills
                        )

                        # Job recommendations
                        recommendations = recommend_jobs(
                            resume_skills
                        )

                        # Learning suggestions
                        suggestions = generate_suggestions(
                            missing_skills
                        )

                        # Store results for display
                        st.session_state["analysis_results"] = {
                            "resume_name": uploaded_file.name,
                            "similarity_score": similarity_score,
                            "skill_score": skill_score,
                            "matched_skills": matched_skills,
                            "missing_skills": missing_skills,
                            "recommendations": recommendations,
                            "suggestions": suggestions
                        }

                        st.success(
                            "Resume analysis completed successfully!"
                        )

            except Exception as e:

                st.error(f"An error occurred: {e}")


    # ======================================
    # 7. DISPLAY ANALYSIS RESULTS
    # ======================================

    if "analysis_results" in st.session_state:

        result = st.session_state["analysis_results"]

        similarity_score = result["similarity_score"]
        skill_score = result["skill_score"]
        matched_skills = result["matched_skills"]
        missing_skills = result["missing_skills"]
        recommendations = result["recommendations"]
        suggestions = result["suggestions"]

        st.divider()

        st.header("📊 Resume Analysis Results")

        st.caption(
            f"Resume: {result['resume_name']}"
        )

        # Metric cards
        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Text Similarity",
                f"{similarity_score}%"
            )

        with col2:

            st.metric(
                "Skill Match",
                f"{skill_score}%"
            )

        with col3:

            st.metric(
                "Matching Skills",
                len(matched_skills)
            )

        with col4:

            st.metric(
                "Missing Skills",
                len(missing_skills)
            )

        st.caption(
            "Text similarity and skill match are separate "
            "keyword-based indicators, not official ATS scores."
        )

        # ==================================
        # 8. SIMILARITY GAUGE
        # ==================================

        st.subheader("📈 Resume Similarity Score")

        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=similarity_score,
                number={
                    "suffix": "%"
                },
                title={
                    "text": "Text Similarity"
                },
                gauge={
                    "axis": {
                        "range": [0, 100]
                    },
                    "bar": {
                        "color": "#2563EB"
                    },
                    "steps": [
                        {
                            "range": [0, 50],
                            "color": "#FEE2E2"
                        },
                        {
                            "range": [50, 75],
                            "color": "#FEF3C7"
                        },
                        {
                            "range": [75, 100],
                            "color": "#DCFCE7"
                        }
                    ]
                }
            )
        )

        gauge.update_layout(
            height=300,
            margin=dict(l=30, r=30, t=60, b=20)
        )

        st.plotly_chart(
            gauge,
            use_container_width=True
        )

        # ==================================
        # 9. SKILL ANALYSIS
        # ==================================

        st.divider()

        st.header("🎯 Skills Analysis")

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("✅ Matching Skills")

            if matched_skills:

                for skill in matched_skills:

                    st.success(skill)

            else:

                st.info("No matching skills found.")

        with col2:

            st.subheader("❌ Missing Skills")

            if missing_skills:

                for skill in missing_skills:

                    st.warning(skill)

            else:

                st.success("No missing skills found!")

        # ==================================
        # 10. SKILL PIE CHART
        # ==================================

        if matched_skills or missing_skills:

            st.subheader("📊 Matching vs Missing Skills")

            pie_chart = go.Figure(
                data=[
                    go.Pie(
                        labels=[
                            "Matching Skills",
                            "Missing Skills"
                        ],
                        values=[
                            len(matched_skills),
                            len(missing_skills)
                        ],
                        hole=0.45
                    )
                ]
            )

            pie_chart.update_layout(
                height=350
            )

            st.plotly_chart(
                pie_chart,
                use_container_width=True
            )

        # ==================================
        # 11. JOB RECOMMENDATIONS
        # ==================================

        st.divider()

        st.header("💼 Recommended Job Roles")

        for role in recommendations:

            with st.container(border=True):

                st.subheader(role["Job Role"])

                st.progress(
                    role["Match Percentage"] / 100
                )

                st.metric(
                    "Keyword Match",
                    f"{role['Match Percentage']}%"
                )

                st.write(
                    "**Matching Skills:**"
                )

                st.write(
                    ", ".join(role["Matching Skills"])
                    if role["Matching Skills"]
                    else "None"
                )

                st.write(
                    "**Missing Skills:**"
                )

                st.write(
                    ", ".join(role["Missing Skills"])
                    if role["Missing Skills"]
                    else "None"
                )

        st.caption(
            "Job recommendation percentages are based on "
            "predefined skill lists. They are not hiring "
            "probabilities."
        )

        # ==================================
        # 12. LEARNING SUGGESTIONS
        # ==================================

        st.divider()

        st.header("📚 Resume Improvement Suggestions")

        if suggestions:

            for skill, tips in suggestions.items():

                with st.expander(
                    f"📖 Improve: {skill}",
                    expanded=True
                ):

                    for tip in tips:

                        st.write(f"📌 {tip}")

        else:

            st.success(
                "Great! No missing skills found in this job description."
            )

        # ==================================
        # 13. DOWNLOAD REPORT
        # ==================================

        st.divider()

        st.header("📥 Download Analysis Report")

        report = f"""
RESUMEAI - RESUME ANALYSIS REPORT

Resume Name: {result['resume_name']}

TEXT SIMILARITY: {similarity_score}%

SKILL MATCH: {skill_score}%

MATCHING SKILLS:
{', '.join(matched_skills) if matched_skills else 'None'}

MISSING SKILLS:
{', '.join(missing_skills) if missing_skills else 'None'}

RECOMMENDED JOB ROLES:
"""

        for role in recommendations:

            report += f"""

Job Role: {role['Job Role']}
Match Percentage: {role['Match Percentage']}%

Matching Skills:
{', '.join(role['Matching Skills']) if role['Matching Skills'] else 'None'}

Missing Skills:
{', '.join(role['Missing Skills']) if role['Missing Skills'] else 'None'}
"""

        report += "\nLEARNING SUGGESTIONS:\n"

        for skill, tips in suggestions.items():

            report += f"\n{skill}:\n"

            for tip in tips:

                report += f"- {tip}\n"

        report += """
Note:
These percentages are keyword-based estimates.
They do not represent actual hiring probabilities.
"""

        st.download_button(
            "📥 Download Resume Analysis Report",
            data=report,
            file_name="ResumeAI_Analysis_Report.txt",
            mime="text/plain",
            use_container_width=True
        )


# ==========================================
# 14. ANALYSIS HISTORY PAGE
# ==========================================

elif page == "Analysis History":

    st.header("🗄️ Previous Analysis History")

    history = get_analysis_history()

    if history:

        history_data = []

        for record in history:

            history_data.append({

                "ID": record[0],

                "Resume Name": record[1],

                "Text Similarity": f"{record[3]}%",

                "Skill Match": f"{record[4]}%",

                "Matching Skills": record[5],

                "Missing Skills": record[6],

                "Analysis Date": record[7]

            })

        history_df = pd.DataFrame(history_data)

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Total saved analyses: {len(history_data)}"
        )

    else:

        st.info("No previous analysis records found.")


# ==========================================
# 15. ABOUT PROJECT PAGE
# ==========================================

elif page == "About Project":

    st.header("ℹ️ About ResumeAI")

    st.write(
        "ResumeAI is a Python-based resume analysis and "
        "job matching application designed to help candidates "
        "understand how their skills align with job descriptions."
    )

    st.subheader("Technologies Used")

    technologies = [
        "Python",
        "Streamlit",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "TF-IDF and Cosine Similarity",
        "Plotly",
        "SQLite",
        "PyPDF"
    ]

    for technology in technologies:

        st.write(f"🔹 {technology}")

    st.subheader("Main Features")

    st.write("""
    - Upload PDF resumes.
    - Extract resume text.
    - Identify technical skills.
    - Compare resume and job description.
    - Calculate keyword-based skill matching.
    - Recommend suitable job roles.
    - Suggest skills to improve.
    - Save analysis history in SQLite.
    - Download analysis reports.
    """)

    st.info(
        "This is a portfolio project. Its similarity and "
        "matching scores are estimates, not official ATS scores "
        "or predictions of hiring outcomes."
    )


# ==========================================
# 16. FOOTER
# ==========================================

st.divider()

st.markdown(
    "<center>📄 ResumeAI | Built with Python and Streamlit</center>",
    unsafe_allow_html=True
)

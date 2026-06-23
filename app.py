import os
import streamlit as st
from groq import Groq
from fpdf import FPDF
import base64
import fitz

st.set_page_config(page_title="AI Career Counselor", page_icon="🎓", layout="wide")



st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #0d0c1a 0%, #15132b 100%);
}
.main .block-container {
    padding-top: 2rem;
    max-width: 1100px;
}
h1 {
    color: #c4b5fd !important;
    text-align: center;
    font-size: 2.6rem !important;
    font-weight: 700 !important;
    margin-bottom: 0.3rem !important;
    text-shadow: 0 0 20px rgba(168, 139, 250, 0.4);
}
.stMarkdown p {
    color: #a5a3c9 !important;
    text-align: center;
    font-size: 1.05rem;
    margin-bottom: 1.5rem;
}
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stSelectbox"] > div {
    border-radius: 12px !important;
    border: 1px solid #3a3666 !important;
    background: linear-gradient(145deg, #1c1a35, #211e3f) !important;
    color: #e8e6ff !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.05) !important;
}
div[data-testid="stTextInput"] label,
div[data-testid="stTextArea"] label,
div[data-testid="stSelectbox"] label {
    font-weight: 600 !important;
    color: #b8b3ff !important;
    font-size: 0.95rem !important;
}
.stButton button {
    background: linear-gradient(145deg, #7c6ff0, #5b4fd1);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.6rem 1.8rem;
    font-weight: 600;
    font-size: 0.95rem;
    box-shadow: 0 4px 15px rgba(124, 111, 240, 0.4), inset 0 1px 0 rgba(255,255,255,0.2);
    transition: all 0.2s;
}
.stButton button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(124, 111, 240, 0.5), inset 0 1px 0 rgba(255,255,255,0.2);
}
.stTabs [data-baseweb="tab-list"] {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    background: linear-gradient(145deg, #1c1a35, #18162e);
    padding: 12px;
    border-radius: 16px;
    border: 1px solid #2e2b54;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
}
.stTabs [data-baseweb="tab"] {
    background: #211e3f;
    border-radius: 10px;
    padding: 10px 16px;
    font-weight: 600;
    color: #9b97c9;
    border: 1px solid #322d5c;
    flex: 1 1 30%;
    text-align: center;
    justify-content: center;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(145deg, #7c6ff0, #5b4fd1) !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(124, 111, 240, 0.5), inset 0 1px 0 rgba(255,255,255,0.2);
}
div[data-testid="stSuccess"] {
    background: linear-gradient(145deg, #1c1a35, #211e3f);
    border-radius: 14px;
    border-left: 4px solid #7c6ff0;
    padding: 1rem 1.2rem;
    color: #e8e6ff;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}
div[data-testid="stWarning"] {
    border-radius: 14px;
}
div[data-testid="stMarkdownContainer"] p {
    color: #d4d2eb;
}
</style>
""", unsafe_allow_html=True)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

st.title("🎓 AI Career Counselor")
st.write("Enter your details and I will suggest the best career options for you!")

name = st.text_input("👤 Your Name:")
qualification = st.selectbox("🎓 Qualification:", ["12th Pass", "Graduate", "Post Graduate"])
skills = st.text_area("⚡ Your Skills (separate by comma):")
interest = st.text_area("❤️ Your Interests:")

def generate_pdf(title, content, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=title, ln=True, align='C')
    pdf.multi_cell(0, 10, txt=content)
    pdf_output = pdf.output(dest='S').encode('latin-1')
    b64 = base64.b64encode(pdf_output).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">📥 Download PDF</a>'
    st.markdown(href, unsafe_allow_html=True)

def ask_groq(prompt):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "🎯 Career Suggestions",
    "🗺️ Learning Roadmap",
    "💼 Interview Questions",
    "🔍 Skills Gap Analyzer",
    "📄 Resume Analyzer",
    "🎓 Course Recommender",
    "💰 Salary Comparison",
    "📝 Resume Tips",
    "📊 Job Market Trends"
])

with tab1:
    if st.button("Suggest Career!"):
        if skills and interest:
            prompt = f"""
            Student Name: {name}
            Qualification: {qualification}
            Skills: {skills}
            Interest: {interest}
            Suggest 5 best career options with Career name, Salary range, Required skills, Future scope.
            Reply in English only.
            """
            result = ask_groq(prompt)
            st.success("Career Suggestions For You:")
            st.write(result)
            generate_pdf("AI Career Counselor - Career Suggestions", result, "career_suggestions.pdf")
        else:
            st.warning("Please fill Skills and Interest!")

with tab2:
    career_goal = st.text_input("🗺️ Enter your Dream Career:")
    if st.button("Generate Roadmap!"):
        if career_goal:
            prompt = f"""
            Create a detailed step by step learning roadmap for someone who wants to become a {career_goal}.
            Current qualification: {qualification}
            Current skills: {skills}
            Include Phase wise plan, Free resources, Timeline, Key skills.
            Reply in English only.
            """
            result = ask_groq(prompt)
            st.success("Your Learning Roadmap:")
            st.write(result)
            generate_pdf("AI Career Counselor - Learning Roadmap", result, "roadmap.pdf")
        else:
            st.warning("Please enter your dream career!")

with tab3:
    career_interview = st.text_input("💼 Enter Career for Interview Questions:")
    if st.button("Generate Interview Questions!"):
        if career_interview:
            prompt = f"""
            Generate 10 important interview questions with answers for {career_interview} position.
            Include both technical and HR questions.
            Reply in English only.
            """
            result = ask_groq(prompt)
            st.success("Interview Questions:")
            st.write(result)
            generate_pdf("AI Career Counselor - Interview Questions", result, "interview_questions.pdf")
        else:
            st.warning("Please enter a career!")

with tab4:
    dream_career = st.text_input("🔍 Enter your Dream Career for Skills Gap Analysis:")
    if st.button("Analyze Skills Gap!"):
        if dream_career and skills:
            prompt = f"""
            Dream Career: {dream_career}
            Current Skills: {skills}
            Current Qualification: {qualification}
            Analyze the skills gap and tell:
            - Skills I already have that are useful
            - Skills I am missing
            - How to learn missing skills
            - Timeline to be job ready
            Reply in English only.
            """
            result = ask_groq(prompt)
            st.success("Skills Gap Analysis:")
            st.write(result)
            generate_pdf("AI Career Counselor - Skills Gap Analysis", result, "skills_gap.pdf")
        else:
            st.warning("Please fill Skills and Dream Career!")

with tab5:
    st.write("Upload your Resume and AI will analyze it!")
    uploaded_file = st.file_uploader("📄 Upload Resume (PDF only)", type="pdf")
    if st.button("Analyze Resume!"):
        if uploaded_file:
            pdf_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            resume_text = ""
            for page in pdf_doc:
                resume_text += page.get_text()
            prompt = f"""
            Analyze this resume and provide:
            - Current skills identified
            - Suggested career options
            - Resume improvement tips
            - Missing skills to add
            Resume Content: {resume_text}
            Reply in English only.
            """
            result = ask_groq(prompt)
            st.success("Resume Analysis:")
            st.write(result)
            generate_pdf("AI Career Counselor - Resume Analysis", result, "resume_analysis.pdf")
        else:
            st.warning("Please upload a PDF resume!")

with tab6:
    course_career = st.text_input("🎓 Enter Career for Course Recommendations:")
    if st.button("Recommend Courses!"):
        if course_career:
            prompt = f"""
            Recommend top free and paid online courses for someone who wants to become a {course_career}.
            Current skills: {skills}
            Include Course name, Platform, Duration, Free or Paid, Why helpful.
            Reply in English only.
            """
            result = ask_groq(prompt)
            st.success("Recommended Courses:")
            st.write(result)
            generate_pdf("AI Career Counselor - Course Recommendations", result, "courses.pdf")
        else:
            st.warning("Please enter a career!")

with tab7:
    st.write("Compare salaries of different careers!")
    career1 = st.text_input("💰 Enter First Career:")
    career2 = st.text_input("💰 Enter Second Career:")
    career3 = st.text_input("💰 Enter Third Career (optional):")
    if st.button("Compare Salaries!"):
        if career1 and career2:
            prompt = f"""
            Compare salaries of these careers:
            1. {career1}
            2. {career2}
            3. {career3 if career3 else 'Skip'}
            For each career provide Entry level salary, Mid level salary, Senior level salary, Top companies hiring, Job growth rate.
            Reply in English only.
            """
            result = ask_groq(prompt)
            st.success("Salary Comparison:")
            st.write(result)
            generate_pdf("AI Career Counselor - Salary Comparison", result, "salary_comparison.pdf")
        else:
            st.warning("Please enter at least 2 careers!")

with tab8:
    resume_career = st.text_input("📝 Enter your Target Career for Resume Tips:")
    if st.button("Get Resume Tips!"):
        if resume_career:
            prompt = f"""
            Give detailed resume tips for someone applying for {resume_career} position.
            Current skills: {skills}
            Current qualification: {qualification}
            Include What to put in resume summary, Key skills to highlight, Projects to add, Keywords to include, Common mistakes to avoid.
            Reply in English only.
            """
            result = ask_groq(prompt)
            st.success("Resume Tips For You:")
            st.write(result)
            generate_pdf("AI Career Counselor - Resume Tips", result, "resume_tips.pdf")
        else:
            st.warning("Please enter your target career!")

with tab9:
    st.write("Discover which careers are in demand right now!")
    industry = st.selectbox("📊 Select Industry:", [
        "Technology", "Healthcare", "Finance", "Education",
        "Marketing", "Data Science", "Cybersecurity", "Design"
    ])
    if st.button("Show Job Market Trends!"):
        prompt = f"""
        Provide current job market trends for {industry} industry.
        Include Top 5 most in demand jobs, Skills wanted by employers, Salary trends, Future outlook for next 5 years, Top companies hiring.
        Reply in English only.
        """
        result = ask_groq(prompt)
        st.success(f"Job Market Trends - {industry}:")
        st.write(result)
        generate_pdf(f"AI Career Counselor - Job Market Trends {industry}", result, "job_trends.pdf")
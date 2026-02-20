import streamlit as st
import google.generativeai as genai

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="E-Learning Doubt Clearing Assistant",
    page_icon="🎓",
    layout="wide"
)

# ----------------------------
# ANIMATIONS (NO BG CHANGE)
# ----------------------------
st.markdown("""
<style>
button {
    border-radius: 10px !important;
    transition: all 0.3s ease-in-out !important;
}

button:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 12px rgba(0, 100, 255, 0.6);
}

.fade-in {
    animation: fadeIn 1s ease-in;
}

@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# LOAD GEMINI
# ----------------------------
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Add GEMINI_API_KEY in Streamlit Cloud → Settings → Secrets")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")

# ----------------------------
# HEADER
# ----------------------------
st.markdown("<h1 class='fade-in'>🎓 E-Learning Doubt Clearing Assistant</h1>", unsafe_allow_html=True)
st.markdown("Provide real-time, context-aware answers within a course environment.")

# ----------------------------
# INPUT SECTION
# ----------------------------
col1, col2 = st.columns([1, 1.4])

with col1:
    course_topic = st.text_input("Course Topic", placeholder="e.g., Calculus - Derivatives")

    lesson_content = st.text_area(
        "Paste Lesson Content (Context)",
        height=200,
        placeholder="Paste relevant lecture or notes here..."
    )

    student_question = st.text_area(
        "Student Doubt / Question",
        height=100,
        placeholder="What is confusing?"
    )

    explanation_mode = st.selectbox(
        "Explanation Style",
        ["Step-by-Step", "Simple Explanation", "Advanced Detailed"]
    )

    include_example = st.checkbox("Include Example")
    include_practice = st.checkbox("Add Practice Question")

    generate_btn = st.button("📚 Clear Doubt")

# ----------------------------
# GENERATION
# ----------------------------
if generate_btn:

    if not lesson_content or not student_question:
        st.warning("Please provide lesson content and a question.")
        st.stop()

    with st.spinner("Analyzing question and generating answer..."):

        prompt = f"""
You are an expert course tutor.

Course Topic: {course_topic}

Lesson Content:
{lesson_content}

Student Question:
{student_question}

Explain using ONLY the lesson context provided.

Explanation Mode: {explanation_mode}
Include Example: {include_example}
Include Practice Question: {include_practice}

Structure EXACTLY like this:

DIRECT ANSWER:

STEP-BY-STEP EXPLANATION:

EXAMPLE:
(Only if enabled)

PRACTICE QUESTION:
(Only if enabled)

QUICK RECAP:

CONFIDENCE LEVEL:
(How confident are you that this answer is correct based on provided context)
"""

        response = model.generate_content(prompt)
        answer = response.text

    with col2:
        st.markdown("<div class='fade-in'>", unsafe_allow_html=True)

        st.subheader("📘 AI Tutor Response")
        st.markdown(answer)

        st.progress(100)
        st.caption("Doubt Cleared Successfully 🎯")

        st.download_button(
            "⬇ Download Answer",
            answer,
            file_name="doubt_solution.txt",
            mime="text/plain"
        )

        if st.button("🔄 Regenerate Answer"):
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# FOOTER
# ----------------------------
if lesson_content:
    st.caption(f"Lesson Word Count: {len(lesson_content.split())}")
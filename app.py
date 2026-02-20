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
# UI ANIMATIONS (NO BG CHANGE)
# ----------------------------
st.markdown("""
<style>
button {
    border-radius: 10px !important;
    transition: all 0.3s ease-in-out !important;
}
button:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 12px rgba(0, 120, 255, 0.6);
}
.fade-in {
    animation: fadeIn 0.8s ease-in;
}
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}
.chat-box {
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
}
.user-msg {
    background-color: #f0f2f6;
}
.ai-msg {
    background-color: #e8f0ff;
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
# SESSION STATE
# ----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ----------------------------
# HEADER
# ----------------------------
st.markdown("<h1 class='fade-in'>🎓 E-Learning Doubt Clearing Assistant</h1>", unsafe_allow_html=True)
st.markdown("Context-aware AI tutor for structured learning support.")

# ----------------------------
# INPUT PANEL
# ----------------------------
col1, col2 = st.columns([1, 1.5])

with col1:
    course_topic = st.text_input("Course Topic")

    lesson_content = st.text_area(
        "Lesson Content (Context)",
        height=200
    )

    explanation_style = st.selectbox(
        "Explanation Style",
        ["Step-by-Step", "Simple", "Detailed", "Exam-Oriented"]
    )

    include_example = st.checkbox("Include Example")
    include_quiz = st.checkbox("Generate Practice Question")

    if st.button("🗑 Reset Session"):
        st.session_state.chat_history = []
        st.rerun()

# ----------------------------
# CHAT INTERFACE
# ----------------------------
with col2:
    for role, msg in st.session_state.chat_history:
        css_class = "user-msg" if role == "User" else "ai-msg"
        st.markdown(f"<div class='chat-box {css_class}'><b>{role}:</b><br>{msg}</div>", unsafe_allow_html=True)

    student_question = st.chat_input("Ask your doubt here...")

    if student_question:

        if not lesson_content:
            st.warning("Please provide lesson content first.")
            st.stop()

        st.session_state.chat_history.append(("User", student_question))

        with st.spinner("Generating answer..."):

            prompt = f"""
You are an AI course tutor.

Course Topic: {course_topic}

Lesson Content:
{lesson_content}

Student Question:
{student_question}

Explain ONLY using the lesson content provided.

Explanation Style: {explanation_style}
Include Example: {include_example}
Include Quiz: {include_quiz}

Structure EXACTLY like this:

DIRECT ANSWER:

DETAILED EXPLANATION:

EXAMPLE:
(If enabled)

PRACTICE QUESTION:
(If enabled)

COMMON MISTAKE TO AVOID:

QUICK RECAP:

CONFIDENCE SCORE (0-100):
"""

            response = model.generate_content(prompt)
            answer = response.text

        st.session_state.chat_history.append(("AI Tutor", answer))
        st.rerun()

# ----------------------------
# DOWNLOAD SESSION
# ----------------------------
if st.session_state.chat_history:
    full_chat = ""
    for role, msg in st.session_state.chat_history:
        full_chat += f"{role}:\n{msg}\n\n"

    st.download_button(
        "⬇ Download Full Session",
        full_chat,
        file_name="learning_session.txt",
        mime="text/plain"
    )

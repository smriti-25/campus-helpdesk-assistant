"""
app.py
------
BU Campus Assist - Bennett University Campus Helpdesk Assistant
Streamlit frontend (Member 2).

Run with:  python -m streamlit run app.py
"""

import streamlit as st

# ---------------------------------------------------------------------------
# 1. PAGE SETTINGS (must be the first Streamlit command)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="BU Campus Assist",
    page_icon="🎓",
    layout="centered",
)

# ---------------------------------------------------------------------------
# 2. CONNECT TO THE BACKEND
#    - If rag_pipeline.py exists, use the REAL backend.
#    - If it does not exist yet, use the temporary mock backend.
# ---------------------------------------------------------------------------
BACKEND_MODE = "real"
try:
    from rag_pipeline import ask_question
except ModuleNotFoundError as err:
    if err.name == "rag_pipeline":
        from mock_backend import ask_question

        BACKEND_MODE = "demo"
    else:
        st.error(
            f"The backend needs a library that is not installed: '{err.name}'. "
            "Please install it and restart the app."
        )
        st.stop()

# ---------------------------------------------------------------------------
# 3. TITLE AND WELCOME MESSAGE
# ---------------------------------------------------------------------------
st.title("🎓 BU Campus Assist")
st.caption("Your Bennett University campus helpdesk, powered by official documents.")

with st.chat_message("assistant"):
    st.markdown(
        "Hello! 👋 Welcome to **BU Campus Assist**, the Bennett University "
        "campus helpdesk assistant. Ask me about attendance, examinations, the "
        "academic calendar, academic rules and other university policies. "
        "I answer using official university documents and show the source "
        "of every answer."
    )

if BACKEND_MODE == "demo":
    st.warning("Demo mode: answers are temporary placeholders.")
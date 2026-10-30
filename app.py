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
# 3. CONSTANTS AND HELPER FUNCTIONS
# ---------------------------------------------------------------------------
ERROR_MESSAGE = (
    "Sorry, something went wrong while finding your answer. "
    "Please try again in a moment."
)

SUGGESTED_QUESTIONS = [
    "What is the attendance requirement?",
    "When do examinations begin?",
    "Where can I find the academic calendar?",
    "What are the examination rules?",
]


def set_pending_question(question_text: str) -> None:
    """Runs when a suggested-question button is clicked."""
    st.session_state.pending_question = question_text


def clear_chat() -> None:
    """Runs when the Clear chat button is clicked."""
    st.session_state.messages = []
    st.session_state.pending_question = None


def format_source(source) -> str:
    """Turn one source from the backend into a readable line of text."""
    if isinstance(source, dict):
        document = source.get("document") or "Unknown document"
        page = source.get("page")
        if page in (None, ""):
            return f"{document} (page number not available)"
        return f"{document}, page {page}"
    return str(source)


def show_message(message: dict) -> None:
    """Draw one chat message. Assistant messages also show their sources."""
    with st.chat_message(message["role"]):
        if message.get("is_error"):
            st.error(message["content"])
        else:
            st.markdown(message["content"])

        sources = message.get("sources") or []
        if message["role"] == "assistant" and sources:
            with st.expander("📄 Sources", expanded=True):
                for source in sources:
                    st.markdown(f"- {format_source(source)}")


# ---------------------------------------------------------------------------
# 4. SESSION STATE (Streamlit's memory between reruns)
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

# ---------------------------------------------------------------------------
# 5. SIDEBAR: suggested questions and Clear chat
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("🎓 BU Campus Assist")
    st.caption("Bennett University Campus Helpdesk Assistant")

    st.subheader("Suggested questions")
    for i, question_text in enumerate(SUGGESTED_QUESTIONS):
        st.button(
            question_text,
            key=f"suggestion_{i}",
            on_click=set_pending_question,
            args=(question_text,),
            width="stretch",
        )

    st.divider()
    st.button("🗑️ Clear chat", on_click=clear_chat, width="stretch")

# ---------------------------------------------------------------------------
# 6. TITLE AND WELCOME MESSAGE
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

# ---------------------------------------------------------------------------
# 7. SHOW CONVERSATION HISTORY
# ---------------------------------------------------------------------------
for message in st.session_state.messages:
    show_message(message)

# ---------------------------------------------------------------------------
# 8. CHAT INPUT AND ANSWER
# ---------------------------------------------------------------------------
typed_question = st.chat_input("Type your question here...")
question = st.session_state.pending_question or typed_question
st.session_state.pending_question = None

if question:
    user_message = {"role": "user", "content": question}
    st.session_state.messages.append(user_message)
    show_message(user_message)

    try:
        with st.spinner("Searching the official documents..."):
            answer, sources = ask_question(question)
        assistant_message = {
            "role": "assistant",
            "content": answer,
            "sources": sources,
        }
    except Exception as err:
        print(f"Backend error: {err}")  # technical detail goes to the terminal only
        assistant_message = {
            "role": "assistant",
            "content": ERROR_MESSAGE,
            "sources": [],
            "is_error": True,
        }

    st.session_state.messages.append(assistant_message)
    show_message(assistant_message)
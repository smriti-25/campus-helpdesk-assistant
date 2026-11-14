
"""
BU Campus Assist - Bennett University Campus Helpdesk Assistant
Streamlit frontend connected to the real AI/RAG backend.

Run with: python -m streamlit run app.py
"""

import streamlit as st

# 1. PAGE SETTINGS
st.set_page_config(
    page_title="BU Campus Assist",
    page_icon="🎓",
    layout="centered",
)

# 2. CONNECT TO THE REAL AI BACKEND
from campus_assistant import CampusAssistant


@st.cache_resource
def load_assistant():
    """Initialize the AI assistant once and reuse it."""
    return CampusAssistant()


# 3. CONSTANTS
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


# 4. HELPER FUNCTIONS
def set_pending_question(question_text: str):
    st.session_state.pending_question = question_text


def clear_chat():
    st.session_state.messages = []
    st.session_state.pending_question = None


def format_source(source):
    if isinstance(source, dict):
        document = source.get("document", "Unknown document")
        page = source.get("page")

        if page in (None, ""):
            return f"{document} (page number not available)"

        return f"{document}, Page {page}"

    return str(source)


def show_message(message: dict):
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


# 5. SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# 6. SIDEBAR
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

    st.button(
        "🗑️ Clear chat",
        on_click=clear_chat,
        width="stretch",
    )


# 7. TITLE AND WELCOME MESSAGE
st.title("🎓 BU Campus Assist")

st.caption(
    "Your Bennett University campus helpdesk, "
    "powered by official university documents."
)

with st.chat_message("assistant"):
    st.markdown(
        "Hello! 👋 Welcome to **BU Campus Assist**, the Bennett University "
        "campus helpdesk assistant. Ask me about attendance, examinations, "
        "the academic calendar, academic rules and other university policies. "
        "I answer using official university documents and show the sources."
    )


# 8. SHOW CHAT HISTORY
for message in st.session_state.messages:
    show_message(message)


# 9. CHAT INPUT AND REAL BACKEND ANSWER
typed_question = st.chat_input("Type your question here...")

question = st.session_state.pending_question or typed_question
st.session_state.pending_question = None

if question:

    user_message = {
        "role": "user",
        "content": question,
    }

    st.session_state.messages.append(user_message)
    show_message(user_message)

    try:

        with st.spinner("Searching official university documents..."):

            # Load the real AI assistant
            assistant = load_assistant()

            # Ask the question using the RAG backend
            result = assistant.ask(question)

        assistant_message = {
            "role": "assistant",
            "content": result.get("answer", ERROR_MESSAGE),
            "sources": result.get("references", []),
        }

        if not result.get("success", False):
            assistant_message["is_error"] = True

    except Exception as err:

        print(f"Backend error: {err}")

        assistant_message = {
            "role": "assistant",
            "content": ERROR_MESSAGE,
            "sources": [],
            "is_error": True,
        }

    st.session_state.messages.append(assistant_message)
    show_message(assistant_message)

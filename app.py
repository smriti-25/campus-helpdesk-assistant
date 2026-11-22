"""
app.py
------
Campus Helpdesk Assistant (BU Campus Assist)
Bennett University Campus Helpdesk Assistant
Streamlit frontend (Member 2), connected to the RAG backend (Member 1).

Run with:  python -m streamlit run app.py
"""

import streamlit as st

# ---------------------------------------------------------------------------
# 1. PAGE SETTINGS (must be the first Streamlit command)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Campus Helpdesk Assistant",
    page_icon="🎓",
    layout="centered",
)

# ---------------------------------------------------------------------------
# 2. CONNECT TO THE BACKEND
#    - Tries the real CampusAssistant (campus_assistant.py).
#    - If it cannot start (missing files, Ollama not running, etc.),
#      falls back to the temporary mock backend so the UI still works.
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner="Starting the assistant...")
def load_backend():
    """Create the real assistant once. Returns (assistant, error_text)."""
    try:
        from campus_assistant import CampusAssistant

        return CampusAssistant(), None
    except Exception as err:
        return None, f"{type(err).__name__}: {err}"


assistant, backend_error = load_backend()
BACKEND_MODE = "real" if assistant is not None else "demo"

if BACKEND_MODE == "demo":
    from mock_backend import ask_question as mock_ask_question


def ask_backend(question: str):
    """
    Single place where the UI talks to the backend.
    Always returns (answer, sources).
    sources = list of {"document": str, "page": int or None}
    """
    if BACKEND_MODE == "real":
        result = assistant.ask(question)
        return result["answer"], result.get("references", [])
    return mock_ask_question(question)


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
    st.header("🎓 Campus Helpdesk Assistant")
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

    st.divider()
    if BACKEND_MODE == "real":
        st.success("Connected to the real backend.")
    else:
        st.warning("Demo mode: answers are temporary placeholders.")
        with st.expander("Why demo mode?"):
            st.code(backend_error or "Unknown reason")

# ---------------------------------------------------------------------------
# 6. TITLE AND WELCOME MESSAGE
# ---------------------------------------------------------------------------
st.title("🎓 Campus Helpdesk Assistant")
st.caption("Your Bennett University campus helpdesk, powered by official documents.")

with st.chat_message("assistant"):
    st.markdown(
        "Hello! 👋 Welcome to **BU Campus Assist**, the Bennett University "
        "campus helpdesk assistant. Ask me about attendance, examinations, the "
        "academic calendar, academic rules and other university policies. "
        "I answer using official university documents and show the source "
        "of every answer."
    )

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
            answer, sources = ask_backend(question)
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
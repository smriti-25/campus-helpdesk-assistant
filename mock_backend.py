"""
mock_backend.py
---------------
TEMPORARY fake backend, used ONLY to build and test the Streamlit UI.

It does NOT read any university documents and its answers are NOT official.
It is replaced by the real backend (rag_pipeline.py) once that is ready.

Interface (same as the real backend):
    answer, sources = ask_question(question)
        answer  -> str
        sources -> list of dicts: {"document": str, "page": int or None}
"""

import time


def ask_question(question: str):
    """Return a fake (answer, sources) pair after a short delay."""
    time.sleep(1.5)  # pretend the AI is thinking, so the loading spinner is visible

    q = question.lower()

    if "attendance" in q:
        answer = (
            "[DEMO MODE] This is a placeholder answer about attendance. "
            "The real answer will come from the official attendance notification "
            "once the backend is connected."
        )
        sources = [
            {
                "document": "Notification-for-Minimum-Attendance-for-Students.pdf",
                "page": None,
            }
        ]

    elif "calendar" in q or "begin" in q or "start" in q:
        answer = (
            "[DEMO MODE] This is a placeholder answer about dates. "
            "The real answer will come from the Academic Calendar 2026-27."
        )
        sources = [{"document": "Academic-Calendar-2026-27.pdf", "page": None}]

    elif "exam" in q:
        answer = (
            "[DEMO MODE] This is a placeholder answer about examinations. "
            "The real answer will come from the Examination Manual."
        )
        sources = [{"document": "Examination-Manual-2024-25.pdf", "page": None}]

    else:
        answer = (
            "[DEMO MODE] I could not find this information in the official "
            "university documents."
        )
        sources = []

    return answer, sources
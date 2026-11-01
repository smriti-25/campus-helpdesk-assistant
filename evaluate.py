
import csv
from campus_assistant import CampusAssistant


TEST_CASES = [
    {
        "id": 1,
        "category": "Attendance",
        "question": "What is the minimum attendance required to be eligible for the End Semester Examination?",
        "check": lambda answer: "75%" in answer
    },
    {
        "id": 2,
        "category": "Scholarship",
        "question": "What is the university scholarship renewal policy and minimum CGPA required?",
        "check": lambda answer: (
            "could not find" in answer.lower()
            and "scholarship" in answer.lower()
        )
    },
    {
        "id": 3,
        "category": "Academic Rules",
        "question": "What happens if a student fails to meet the minimum academic requirements for promotion to the next year?",
        "check": lambda answer: (
            "year-back" in answer.lower()
            or "re-register" in answer.lower()
        )
    },
    {
    "id": 4,
    "category": "Academic Calendar",
    "question": "What is the last scheduled date for End Semester Examinations in the odd semester 2026-27 calendar?",
    "check": lambda answer: (
        "23 december 2026" in answer.lower()
        or "23-12-2026" in answer.lower()
    )
    },
    {
        "id": 5,
        "category": "Graduation",
        "question": "What is the minimum CGPA required for a student to graduate?",
        "check": lambda answer: (
            "not directly stated" in answer.lower()
            or "not mentioned" in answer.lower()
        )
    },
    {
        "id": 6,
        "category": "Out of Scope",
        "question": "Who is the current Prime Minister of India?",
        "check": lambda answer: "could not find relevant information" in answer.lower()
    }
]


def run_evaluation():

    print("\nInitializing BU Campus Assist...\n")

    assistant = CampusAssistant()

    results = []

    for test in TEST_CASES:

        print("\n" + "=" * 60)
        print("Running Test:", test["id"])
        print("Category:", test["category"])
        print("Question:", test["question"])
        print("=" * 60)

        try:

            result = assistant.ask(test["question"])

            answer = result["answer"]
            references = result["references"]

            passed = test["check"](answer)

            status = "PASS" if passed else "REVIEW"

            print("\nAnswer:", answer)
            print("\nReferences:", references)
            print("\nEvaluation:", status)

            results.append({
                "test_id": test["id"],
                "category": test["category"],
                "question": test["question"],
                "answer": answer,
                "references": str(references),
                "status": status
            })

        except Exception as error:

            print("\nTest Error:", error)

            results.append({
                "test_id": test["id"],
                "category": test["category"],
                "question": test["question"],
                "answer": str(error),
                "references": "",
                "status": "ERROR"
            })

    # Save evaluation results

    with open(
        "evaluation_results.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        fieldnames = [
            "test_id",
            "category",
            "question",
            "answer",
            "references",
            "status"
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(results)

    # Display summary

    passed_count = sum(
        1 for result in results
        if result["status"] == "PASS"
    )

    review_count = sum(
        1 for result in results
        if result["status"] == "REVIEW"
    )

    error_count = sum(
        1 for result in results
        if result["status"] == "ERROR"
    )

    total = len(results)

    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)

    print("Total Tests:", total)
    print("Passed:", passed_count)
    print("Needs Review:", review_count)
    print("Errors:", error_count)

    print(
        "Rule-check pass rate:",
        round((passed_count / total) * 100, 2),
        "%"
    )

    print("\nResults saved to evaluation_results.csv")


if __name__ == "__main__":
    run_evaluation()

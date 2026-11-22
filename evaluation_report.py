
import pandas as pd
import matplotlib.pyplot as plt

# Load existing evaluation results
df = pd.read_csv("evaluation_results.csv")

# Calculate summary
total = len(df)
passed = (df["status"] == "PASS").sum()
review = (df["status"] == "REVIEW").sum()
errors = (df["status"] == "ERROR").sum()

pass_rate = (passed / total) * 100 if total else 0

print("\nBU CAMPUS ASSIST - EVALUATION REPORT")
print("=" * 50)

print("Total Test Cases:", total)
print("Passed:", passed)
print("Needs Review:", review)
print("Errors:", errors)
print("Rule-check Pass Rate:", round(pass_rate, 2), "%")

print("\nCATEGORY-WISE RESULTS")
print("-" * 50)

category_results = df.groupby(
    ["category", "status"]
).size().unstack(fill_value=0)

print(category_results)

# Save summary
summary = pd.DataFrame({
    "Metric": [
        "Total Test Cases",
        "Passed",
        "Needs Review",
        "Errors",
        "Rule-check Pass Rate (%)"
    ],
    "Value": [
        total,
        passed,
        review,
        errors,
        round(pass_rate, 2)
    ]
})

summary.to_csv("evaluation_summary.csv", index=False)

# Plot 1: Evaluation status
status_counts = df["status"].value_counts()

plt.figure(figsize=(7, 5))
status_counts.plot(kind="bar")
plt.title("BU Campus Assist - Evaluation Status")
plt.xlabel("Evaluation Status")
plt.ylabel("Number of Test Cases")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("evaluation_status.png")
plt.show()

# Plot 2: Category-wise results
category_results.plot(
    kind="bar",
    figsize=(9, 5)
)

plt.title("Category-wise Evaluation Results")
plt.xlabel("Category")
plt.ylabel("Number of Test Cases")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("category_results.png")
plt.show()

print("\nGenerated files:")
print("1. evaluation_summary.csv")
print("2. evaluation_status.png")
print("3. category_results.png")

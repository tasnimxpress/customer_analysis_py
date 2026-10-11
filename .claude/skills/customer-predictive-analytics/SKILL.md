---
name: customer-predictive-analytics
description: End-to-end predictive customer analytics in Python — picks the right method (linear regression for numeric targets like sales/revenue, logistic regression for yes/no outcomes like churn, k-means clustering for customer segmentation), runs it, and delivers a reproducible Python script, an Excel workbook of results, and a plain-language business summary, while teaching the user the concepts step by step. Use this skill whenever the user wants to predict, forecast, explain drivers of, classify, or segment customers, stores, or sales from a CSV/Excel dataset — e.g. "what drives store sales", "which customers will churn", "segment my customers", "run a regression on this", "cluster this data", "build a churn model" — or asks to learn/understand regression, logistic regression, clustering, or predictive analytics, even if they don't name a specific method.
---

# Customer Predictive Analytics

This skill turns a customer/business dataset into a finished predictive analysis **and** teaches the user how it works along the way. The user is learning these techniques, so every analysis is also a lesson: explain the *why* behind each step in plain language, not just the code.

## Deliverables (every run)

1. **Python script** (`analysis/<dataset>_<method>.py`) — reproducible, commented so a learner can follow it top to bottom. Prefer a `.py` script; produce a Jupyter notebook (`.ipynb`) instead if the user asks for one.
2. **Excel workbook** (`analysis/<dataset>_<method>_results.xlsx`) — built with `scripts/excel_report.py` (see below), so results look consistent across analyses.
3. **Written summary** in the chat (and saved as `analysis/<dataset>_<method>_summary.md`) — findings, business recommendations, and a short "What you learned" section.

Put outputs in an `analysis/` folder next to the raw data unless the user names another place. Never modify the raw data files.

## Workflow

### 0. Environment check
Run once at the start:
```bash
python -c "import pandas, sklearn, openpyxl, matplotlib, statsmodels"
```
If anything is missing, install it (`python -m pip install pandas scikit-learn openpyxl matplotlib statsmodels`) and tell the user what you installed and why each library is needed (one line each).

### 1. Understand the data and the question
Load the file and show the user: row/column count, column types, missing values, and a few sample rows. Then restate the business question in one sentence. If the goal is ambiguous (e.g. "analyze this"), propose the most sensible question given the columns and say so — don't stall.

### 2. Choose the method
| What the user wants | Target column | Method | Reference |
|---|---|---|---|
| Predict/explain a **number** (sales, spend, revenue) | numeric | Linear regression | `references/regression.md` |
| Predict a **yes/no** outcome (churn, buy, respond) | binary | Logistic regression | `references/classification.md` |
| Find **groups** of similar customers | none | K-means clustering | `references/clustering.md` |

Read the matching reference file before writing code — it has the prep steps, metrics, pitfalls, and interpretation guidance for that method. Tell the user which method you chose and why, in terms of the table above (this decision is itself one of the most important things to learn).

### 3. Prepare the data
Common steps (method-specific details are in the reference):
- Drop pure ID columns (`Customer_ID`, `Store_ID`, `CustomerID`) — they carry no predictive meaning and can mislead the model.
- Handle missing values; report how many and what you did.
- One-hot encode categorical columns (`pd.get_dummies(..., drop_first=True)`), and explain the "baseline category" this creates.
- Convert dates into useful numbers (e.g. store age in years) rather than dropping them silently.
- Watch for high-cardinality text columns (e.g. `City` with hundreds of values) — usually drop or group them and say why.

### 4. Build and evaluate the model
Follow the reference file. Always use `random_state=42` so results are reproducible. For supervised models, use a train/test split (70/30 by default) and report metrics on the **test** set.

### 5. Write the deliverables
- **Script**: sections with headers (`# --- 1. Load data ---` etc.), each preceded by a short comment explaining the concept, not just the action. It must run standalone with `python <script>.py` from the repo root using relative paths.
- **Excel**: call the helper from your script:
  ```python
  import sys; sys.path.insert(0, r"<path-to-this-skill>/scripts")
  from excel_report import write_report
  write_report(path, sheets={"Coefficients": df, ...}, summary={"R²": 0.62, ...},
               notes=["plain-language takeaway", ...], images={"Charts": ["chart.png", ...]})
  ```
  The docstring in `scripts/excel_report.py` explains each argument. Typical sheets: `Summary` (key metrics + plain-language notes), `Data_Prepared`, `Coefficients` or `Cluster_Profiles`, `Predictions` (test set actual vs predicted, or each customer's cluster), and charts embedded as images.
- **Summary**: use the template below.

Run the script yourself and confirm it completes and the workbook opens (load it with openpyxl) before reporting results. Report real numbers from the run — never invented ones.

### 6. Teach
The user explicitly wants to learn these skills. Teaching is woven in, not bolted on:
- Before each workflow step, give a 1–3 sentence explanation of what the step is and why it matters.
- When a metric appears for the first time (R², p-value, precision, recall, silhouette…), define it in plain words and interpret *this* value ("R² = 0.62 means the model explains about 62% of the variation in sales").
- End with the "What you learned" section and 2–3 **practice questions** the user can try on their own (e.g. "Remove `Parking_Space` and rerun — does R² change much? What does that tell you?"). Offer to check their answers.
- `references/teaching.md` has analogies, a concept glossary, and common learner misconceptions — read it when explaining a concept for the first time or when the user asks "what does X mean?".

If the user asks only a conceptual question (no dataset), skip the deliverables and teach directly, using a small example from their own data where possible.

## Summary template

```markdown
# <Business question>

**Method:** <method> — <one-line why>
**Data:** <rows> rows, <features used> features (<what was dropped and why>)

## Key results
- <metric>: <value> — <plain-language meaning>
- ...

## What drives the outcome / What the segments look like
<Top 3–5 drivers or segment profiles, each with direction, size, and business meaning>

## Recommendations
1. <Actionable, tied to a specific finding>
2. ...

## Caveats
<Correlation ≠ causation, data limits, model weaknesses you observed>

## What you learned
<3–5 bullets on concepts this analysis used>

## Practice questions
1. ...
```

## Principles
- **Honesty over polish**: if a model is weak (low R², accuracy no better than always guessing the majority class), say so plainly and explain what that means — a weak model is a valid, teachable finding.
- **Business language first**: lead with what it means for the business, then the statistics.
- **Correlation, not causation**: coefficients describe associations in this data, not proof that changing X will change Y.

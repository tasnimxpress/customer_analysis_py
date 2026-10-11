# Logistic Regression (yes/no outcomes, e.g. churn)

Use when the target has two values (TRUE/FALSE, Yes/No, 1/0).

## Prep
- Convert the target to 0/1 explicitly and state which value is "1" (the positive class, e.g. churned = 1).
- **Check class balance first** (`y.value_counts(normalize=True)`). This sets the baseline: if 58% didn't churn, a model that always says "no churn" is already 58% accurate. The model must beat that.
- Boolean features → int; categoricals → one-hot with `drop_first=True`.
- **Scale numeric features** (`StandardScaler`, fit on train only — fitting on all data leaks test information). Scaling helps the solver converge and makes coefficients comparable across features.
- Use `train_test_split(..., stratify=y, random_state=42)` so both sets keep the same churn rate.

## Model
- `LogisticRegression(max_iter=1000)` inside a `Pipeline` with the scaler.
- Optionally also fit `statsmodels.api.Logit` for p-values when interpretation matters.

## Evaluate (test set)
- **Baseline accuracy** (majority class) vs model accuracy — always show both.
- **Confusion matrix** — explain each cell in business terms (e.g. false negative = a churner we failed to flag).
- **Precision** (of those flagged, how many really churn) and **recall** (of real churners, how many we caught). Discuss which matters more for the business: missing a churner usually costs more than an unnecessary retention offer.
- **ROC AUC** — the probability the model ranks a random churner above a random non-churner; 0.5 = coin flip.
- Mention the **threshold**: 0.5 is a default, not a law. Show how precision/recall shift at e.g. 0.3 if recall is low.

## Interpretation
- Coefficients are in log-odds; convert to **odds ratios** with `np.exp(coef)`. On scaled features: "a one-standard-deviation increase in X multiplies the odds of churn by ≈ OR".
- OR > 1 raises churn risk, OR < 1 lowers it.
- Output per-customer **churn probabilities** — the most actionable artifact (a ranked list for a retention team).

## Weak-model case
If AUC ≈ 0.5 or accuracy ≈ baseline, say so clearly: the available features don't separate churners well. That's a real finding (common with synthetic datasets). Suggest what data might help, and teach why the result looks this way rather than over-claiming the drivers.

## Excel sheets
`Summary` (accuracy, baseline, precision, recall, AUC), `Confusion_Matrix`, `Coefficients` (coef, odds ratio, direction), `Predictions` (customer id, actual, predicted probability, predicted class — sorted by risk), `Data_Prepared`, charts (confusion-matrix heatmap, ROC curve, odds-ratio bar chart).

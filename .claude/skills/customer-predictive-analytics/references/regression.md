# Linear Regression

Use when the target is a continuous number (sales, spend, revenue, time).

## Prep
- Target `y` = the numeric column; features `X` = everything else after dropping IDs.
- Dates → numbers: e.g. `Store_Age_Years = (reference_date - Opening_Date).days / 365.25`. Parse with an explicit format (check whether it's `%d-%m-%Y` or `%m-%d-%Y` by looking for day values > 12).
- One-hot encode categoricals with `drop_first=True` to avoid the "dummy variable trap" (perfectly redundant columns).
- High-cardinality columns (e.g. `City`, hundreds of values): drop, or keep a coarser version (`State`) — explain that too many dummies with little data per level leads to overfitting.

## Model
Fit **both**, because they answer different questions:
1. `statsmodels.api.OLS(y_train, sm.add_constant(X_train))` — for interpretation: coefficients, standard errors, p-values, confidence intervals. Cast X to float first (`X.astype(float)`) since bool dummies break statsmodels.
2. `sklearn.linear_model.LinearRegression` — for prediction on the test set.

## Evaluate (on test set)
- **R²** — share of variation in y explained. Context matters: 0.3 can be useful for noisy human behavior; 0.95 on business data may signal leakage.
- **RMSE** — typical prediction error in the target's own units (e.g. dollars). Compare it to the mean of y to give it scale.
- **MAE** — average absolute error; less sensitive to outliers than RMSE.
- Compare train vs test R²: a big drop means overfitting.

## Diagnostics (brief, with one chart each)
- **Actual vs predicted** scatter with a 45° line.
- **Residuals vs predicted** — should look like a random cloud; a funnel or curve means the linear assumptions are strained.
- **Multicollinearity** — compute VIF (`statsmodels.stats.outliers_influence.variance_inflation_factor`); VIF > 10 means a feature overlaps heavily with others, so its coefficient is unstable.

## Interpretation
- Coefficient: "holding everything else constant, each 1-unit increase in X is associated with a ≈ β change in y". For dummies: "compared to the baseline category".
- p-value < 0.05: the association is unlikely to be pure noise. Not the same as "important" — check the size too.
- To rank drivers fairly across different units, also show **standardized coefficients** (fit on z-scored X) or the effect of a one-standard-deviation change.

## Excel sheets
`Summary`, `Coefficients` (feature, coef, std err, p-value, CI low/high, significant Y/N), `Predictions` (actual, predicted, residual), `Data_Prepared`, charts.

## Pitfalls to mention when relevant
- Leakage: features computed from the target, or known only after the outcome.
- Extrapolation: predictions outside the range of the training data are unreliable.
- Outliers can pull the line; check the largest residuals.

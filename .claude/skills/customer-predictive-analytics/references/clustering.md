# K-Means Clustering (customer segmentation)

Use when there is no target and the user wants groups of similar customers.

## Prep
- Choose features that reflect the segmentation goal (e.g. `Annual Income`, `Spending Score` for marketing segments). More features is not automatically better: distances get noisy. State which features you used and why.
- Drop IDs. Categoricals (e.g. Gender) usually stay out of k-means (distance on 0/1 dummies is awkward); profile them *after* clustering instead.
- **Scale** with `StandardScaler`. K-means uses distance, so an unscaled income in thousands would swamp a 1–100 score.

## Choosing k
- **Elbow plot**: inertia (within-cluster spread) for k = 2..10; look for where gains flatten.
- **Silhouette score** for each k (−1 to 1; higher = better-separated clusters; > 0.5 is strong, 0.25–0.5 is reasonable).
- Choose k using both plus business sense (can marketing act on 5 segments? on 9?). Explain the choice.
- `KMeans(n_clusters=k, n_init=10, random_state=42)`.

## Profile the clusters
- Mean of each feature per cluster **in original units** (not scaled), plus size (count and %) and the mix of excluded categoricals (e.g. % female).
- Give each cluster a **descriptive name** ("High income, low spend — 'Careful affluent'") and one marketing action.
- If there are 2 features, plot a scatter colored by cluster with centroids. With more features, plot the first two PCA components and say that's what the axes are.

## Caveats
- K-means assumes roughly round, similar-sized clusters, and results depend on k and the features chosen.
- Clusters are descriptive, not predictive truths; validate them with the business.

## Excel sheets
`Summary` (k chosen, silhouette, rationale), `Cluster_Profiles` (one row per cluster: name, size, feature means, action), `Customer_Segments` (each customer + cluster label + cluster name), `K_Selection` (k, inertia, silhouette), charts (elbow, silhouette, cluster scatter).

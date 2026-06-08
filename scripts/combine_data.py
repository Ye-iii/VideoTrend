import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# =========================
# INPUT FILES
# =========================

youtube_path = os.path.join(
    BASE_DIR,
    "data",
    "formatted",
    "youtube",
    "youtube_formatted.parquet"
)

trends_path = os.path.join(
    BASE_DIR,
    "data",
    "formatted",
    "trends",
    "trends_formatted.parquet"
)

# =========================
# OUTPUT
# =========================

output_dir = os.path.join(
    BASE_DIR,
    "data",
    "combined"
)

os.makedirs(output_dir, exist_ok=True)

# =========================
# LOAD DATA
# =========================

youtube_df = pd.read_parquet(youtube_path)
trends_df = pd.read_parquet(trends_path)

print(f"Loaded formatted YouTube data from {youtube_path}")
print(f"Loaded formatted Google Trends data from {trends_path}")

# =========================
# AGGREGATE YOUTUBE DATA
# =========================

youtube_agg = youtube_df.groupby("keyword").agg({
    "view_count": "mean",
    "like_count": "mean",
    "comment_count": "mean"
}).reset_index()

youtube_agg.columns = [
    "keyword",
    "avg_views",
    "avg_likes",
    "avg_comments"
]

# =========================
# AGGREGATE TRENDS DATA
# =========================

trends_agg = trends_df.groupby("keyword").agg({
    "trend_score": "mean"
}).reset_index()

# =========================
# COMBINE DATA
# =========================

final_df = pd.merge(
    youtube_agg,
    trends_agg,
    on="keyword",
    how="inner"
)

final_df["engagement_score"] = (
    final_df["avg_likes"] +
    final_df["avg_comments"]
) / final_df["avg_views"]

numeric_cols = [
    "avg_views",
    "avg_likes",
    "avg_comments",
    "trend_score",
    "engagement_score"
]

for col in numeric_cols:
    final_df[col] = pd.to_numeric(
        final_df[col],
        errors="coerce"
    )

# =========================
# ADD KPI
# =========================

final_df = final_df.replace([float("inf"), float("-inf")], pd.NA)


def min_max_normalize(series):
    min_value = series.min()
    max_value = series.max()

    if pd.isna(min_value) or pd.isna(max_value) or min_value == max_value:
        return 0

    return (series - min_value) / (max_value - min_value)


normalization_cols = {
    "avg_views": "avg_views_norm",
    "avg_likes": "avg_likes_norm",
    "avg_comments": "avg_comments_norm",
    "trend_score": "trend_score_norm",
    "engagement_score": "engagement_score_norm"
}

for source_col, norm_col in normalization_cols.items():
    final_df[norm_col] = min_max_normalize(final_df[source_col])

final_df["final_score"] = (
    0.5 * final_df["trend_score_norm"] +
    0.3 * final_df["avg_views_norm"] +
    0.2 * final_df["engagement_score_norm"]
)

print("Added Min-Max normalization columns and final_score.")

# =========================
# SAVE
# =========================

output_path = os.path.join(
    output_dir,
    "final_dataset.csv"
)

final_df.to_csv(output_path, index=False)

print(f"Final combined dataset saved to {output_path}")
print(final_df)

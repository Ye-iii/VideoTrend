import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# =========================
# INPUT PATHS
# =========================

youtube_input = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "youtube"
)

trends_input = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "trends"
)

# =========================
# OUTPUT PATHS
# =========================

youtube_output = os.path.join(
    BASE_DIR,
    "data",
    "formatted",
    "youtube"
)

trends_output = os.path.join(
    BASE_DIR,
    "data",
    "formatted",
    "trends"
)

os.makedirs(youtube_output, exist_ok=True)
os.makedirs(trends_output, exist_ok=True)


def get_latest_csv(input_dir):
    csv_files = sorted(
        f for f in os.listdir(input_dir)
        if f.lower().endswith(".csv")
    )

    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {input_dir}")

    return csv_files[-1]

# =========================
# FORMAT YOUTUBE DATA
# =========================

youtube_file = get_latest_csv(youtube_input)

youtube_path = os.path.join(youtube_input, youtube_file)

print(f"Selected YouTube raw file: {youtube_file}")

youtube_df = pd.read_csv(youtube_path)

# remove duplicates
youtube_df = youtube_df.drop_duplicates()

# convert dates
youtube_df["published_at"] = pd.to_datetime(
    youtube_df["published_at"],
    errors="coerce"
)

youtube_df["collected_at"] = pd.to_datetime(
    youtube_df["collected_at"],
    errors="coerce"
)

# standardize column names
youtube_df.columns = youtube_df.columns.str.lower()

# fill missing values
youtube_df = youtube_df.fillna(0)

youtube_output_path = os.path.join(
    youtube_output,
    "youtube_formatted.parquet"
)

youtube_df.to_parquet(youtube_output_path, index=False)

print(f"YouTube formatted data saved to {youtube_output_path}")

# =========================
# FORMAT GOOGLE TRENDS DATA
# =========================

trends_file = get_latest_csv(trends_input)

trends_path = os.path.join(trends_input, trends_file)

print(f"Selected Google Trends raw file: {trends_file}")

trends_df = pd.read_csv(trends_path)

# remove duplicates
trends_df = trends_df.drop_duplicates()

# convert dates
trends_df["date"] = pd.to_datetime(
    trends_df["date"],
    errors="coerce"
)

trends_df["collected_at"] = pd.to_datetime(
    trends_df["collected_at"],
    errors="coerce"
)

# standardize columns
trends_df.columns = trends_df.columns.str.lower()

# fill missing values
trends_df = trends_df.fillna(0)

trends_output_path = os.path.join(
    trends_output,
    "trends_formatted.parquet"
)

trends_df.to_parquet(trends_output_path, index=False)

print(f"Google Trends formatted data saved to {trends_output_path}")

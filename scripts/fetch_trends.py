import os
from datetime import datetime
import pandas as pd
from pytrends.request import TrendReq

KEYWORDS = [
    "AI",
    "Green Tech",
    "Oil Price",
    "Electric Vehicles",
    "Renewable Energy"
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "raw", "trends")

os.makedirs(OUTPUT_DIR, exist_ok=True)

today = datetime.now().strftime("%Y-%m-%d")
output_filename = f"google_trends_raw_{today}.csv"
output_path = os.path.join(OUTPUT_DIR, output_filename)

if os.path.exists(output_path):
    print(f"Today's Google Trends raw file already exists: {output_path}")
    print("Skipping Google Trends collection successfully.")
    exit(0)

pytrends = TrendReq(hl='en-US', tz=360)

all_data = []

for keyword in KEYWORDS:
    print(f"Fetching trends for: {keyword}")

    pytrends.build_payload(
        [keyword],
        timeframe='today 12-m',
        geo=''
    )

    df = pytrends.interest_over_time()

    if not df.empty:
        df = df.reset_index()

        for _, row in df.iterrows():
            all_data.append({
                "keyword": keyword,
                "date": row["date"],
                "trend_score": row[keyword],
                "collected_at": datetime.now().isoformat()
            })

final_df = pd.DataFrame(all_data)

final_df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"Saved {len(final_df)} rows to {output_path}")

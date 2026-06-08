import os
import pandas as pd
import requests
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "combined",
    "final_dataset.csv"
)

ES_URL = "http://host.docker.internal:9200"
INDEX_NAME = "video_trends"

df = pd.read_csv(DATA_PATH)
indexed_at = datetime.utcnow().isoformat()

print(f"Loaded final dataset from {DATA_PATH}")
print(f"Indexing {len(df)} rows into Elasticsearch index: {INDEX_NAME}")

mapping = {
    "mappings": {
        "properties": {
            "@timestamp": {"type": "date"},
            "keyword": {"type": "keyword"},
            "avg_views": {"type": "float"},
            "avg_likes": {"type": "float"},
            "avg_comments": {"type": "float"},
            "trend_score": {"type": "float"},
            "engagement_score": {"type": "float"},
            "avg_views_norm": {"type": "float"},
            "avg_likes_norm": {"type": "float"},
            "avg_comments_norm": {"type": "float"},
            "trend_score_norm": {"type": "float"},
            "engagement_score_norm": {"type": "float"},
            "final_score": {"type": "float"}
        }
    }
}

# Create index if needed
create_url = f"{ES_URL}/{INDEX_NAME}"
response = requests.put(
    create_url,
    headers={"Content-Type": "application/json"},
    data=json.dumps(mapping)
)

if response.status_code not in [200, 201, 400]:
    print("Index creation response:", response.text)

# Insert documents
for i, row in df.iterrows():
    document = {
        "@timestamp": indexed_at,
        "keyword": str(row["keyword"]),
        "avg_views": float(row["avg_views"]),
        "avg_likes": float(row["avg_likes"]),
        "avg_comments": float(row["avg_comments"]),
        "trend_score": float(row["trend_score"]),
        "engagement_score": float(row["engagement_score"]),
        "avg_views_norm": float(row["avg_views_norm"]),
        "avg_likes_norm": float(row["avg_likes_norm"]),
        "avg_comments_norm": float(row["avg_comments_norm"]),
        "trend_score_norm": float(row["trend_score_norm"]),
        "engagement_score_norm": float(row["engagement_score_norm"]),
        "final_score": float(row["final_score"])
    }

    doc_id = f"{row['keyword']}_{indexed_at}"
    url = f"{ES_URL}/{INDEX_NAME}/_doc/{doc_id}"
    response = requests.put(
        url,
        headers={"Content-Type": "application/json"},
        data=json.dumps(document)
    )

    if response.status_code not in [200, 201]:
        print("Error inserting row", i, response.text)

refresh_url = f"{ES_URL}/{INDEX_NAME}/_refresh"
requests.post(refresh_url)

print(f"Data indexed successfully at {indexed_at}")
print(f"Kibana can use index pattern '{INDEX_NAME}' with time field '@timestamp'.")

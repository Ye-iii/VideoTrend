import os
from datetime import datetime
import pandas as pd
from googleapiclient.discovery import build

API_KEY = "AIzaSyBEHmKuzYXKoo15vYhgMfAd-eeZ4_AuTB0"

KEYWORDS = [
    "AI",
    "Green Tech",
    "Oil Price",
    "Electric Vehicles",
    "Renewable Energy"
]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "raw", "youtube")
os.makedirs(OUTPUT_DIR, exist_ok=True)

today = datetime.now().strftime("%Y-%m-%d")
output_path = os.path.join(
    OUTPUT_DIR,
    f"youtube_raw_{today}.csv"
)

if os.path.exists(output_path):
    print(f"Today's YouTube raw file already exists: {output_path}")
    print("Skipping YouTube collection successfully.")
    exit(0)

youtube = build("youtube", "v3", developerKey=API_KEY)

all_videos = []

for keyword in KEYWORDS:
    print(f"Searching keyword: {keyword}")

    search_response = youtube.search().list(
        q=keyword,
        part="snippet",
        type="video",
        maxResults=50,
        order="viewCount"
    ).execute()

    video_ids = [item["id"]["videoId"] for item in search_response["items"]]

    videos_response = youtube.videos().list(
        part="snippet,statistics",
        id=",".join(video_ids)
    ).execute()

    for item in videos_response["items"]:
        snippet = item["snippet"]
        stats = item.get("statistics", {})

        all_videos.append({
            "keyword": keyword,
            "video_id": item["id"],
            "title": snippet.get("title"),
            "channel_title": snippet.get("channelTitle"),
            "published_at": snippet.get("publishedAt"),
            "view_count": int(stats.get("viewCount", 0)),
            "like_count": int(stats.get("likeCount", 0)),
            "comment_count": int(stats.get("commentCount", 0)),
            "collected_at": datetime.now().isoformat()
        })

df = pd.DataFrame(all_videos)

df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"Saved {len(df)} rows to {output_path}")
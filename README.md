## Data Sources

- Google Trends data collected through PyTrends
- YouTube video statistics collected through the YouTube Data API

The monitored topics are:

- Artificial Intelligence
- Green Tech
- Oil Price
- Electric Vehicles
- Renewable Energy

## Project Structure

```text
video_trends_project/
├── dags/
│   └── youtube_trends_pipeline.py
├── data/
│   ├── raw/
│   ├── formatted/
│   └── combined/
├── scripts/
│   ├── fetch_trends.py
│   ├── fetch_youtube.py
│   ├── format_data.py
│   ├── combine_data.py
│   └── index_to_elastic.py
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Pipeline Steps
fetch_trends.py collects Google Trends data.
fetch_youtube.py collects YouTube video statistics.
format_data.py cleans the raw data and converts it to Parquet format.
combine_data.py combines both sources and creates KPIs.
index_to_elastic.py indexes the final dataset into Elasticsearch.
Kibana is used to visualize the final results.

## Main KPIs
Trend Score
Average Views
Engagement Score
Final Score

## Technologies Used
Python
Pandas
PyTrends
YouTube Data API
Apache Airflow
Docker
Parquet
Elasticsearch
Kibana

## Output
Final dataset:
data/combined/final_dataset.csv

Elasticsearch index:
video_trends

## Project Blog
A detailed description of the project can be found in:
BLOG_POST.md
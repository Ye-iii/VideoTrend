# Building an End-to-End Big Data Pipeline for Online Video Popularity and Search Trend Analysis

## Introduction

Understanding public interest is important for content creators, businesses, and decision-makers. However, relying on a single platform often provides only a partial view of user behavior.

In this project, we developed a complete Big Data pipeline that combines Google Trends and YouTube data to analyze the popularity and engagement of several technology and energy-related topics.

The topics studied were:

* Artificial Intelligence
* Green Tech
* Oil Price
* Electric Vehicles
* Renewable Energy

Our objective was to compare search interest, video visibility, and user engagement in order to identify the most influential topics.

## Data Sources

Two external data sources were used.

The first source was Google Trends, accessed through the PyTrends library. It provides information about search interest over time.

The second source was the YouTube Data API, which provides video statistics such as views, likes, and comments.

Combining these two sources allowed us to compare what users search for and what they actually watch and interact with.

## Architecture

The project follows a Data Lake architecture composed of three layers:

1. Raw Layer
2. Formatting Layer
3. Combined Layer

Raw data is first collected and stored as CSV files.

The formatting layer cleans the data and converts it into Parquet format to improve storage efficiency and analytical performance.

The combined layer merges the two data sources and calculates analytical indicators.

The workflow is orchestrated using Apache Airflow.

## KPI Calculation

Three key indicators were created:

* Trend Score
* Average Views
* Engagement Score

The engagement score is calculated using likes and comments relative to video views.

After normalization, the indicators are combined into a final score that reflects overall popularity and audience interest.

## Elasticsearch and Kibana

After processing, the final dataset is indexed into Elasticsearch.

Kibana is then used to build interactive dashboards that allow users to explore and compare different topics.

This architecture demonstrates how Big Data technologies can transform raw information into actionable insights.

## Results

The analysis showed that Artificial Intelligence achieved the highest overall score, indicating strong search interest and video visibility.

Renewable Energy ranked second, reflecting growing public attention toward sustainability topics.

Oil Price generated the highest engagement rate despite a lower overall visibility, suggesting a smaller but highly involved audience.

## Conclusion

This project demonstrates a complete Big Data workflow, from data ingestion and transformation to indexing and visualization.

By combining Google Trends, YouTube Data API, Apache Airflow, Elasticsearch, and Kibana, we created an automated analytical platform capable of transforming raw data into meaningful business insights.

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

PROJECT_DIR = "/opt/airflow/video_trends_project"

default_args = {
    "owner": "video_trends_project_ye_tian",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="youtube_google_trends_pipeline",
    default_args=default_args,
    description="YouTube + Google Trends Data Pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    fetch_youtube = BashOperator(
        task_id="fetch_youtube",
        bash_command=f"cd {PROJECT_DIR} && python scripts/fetch_youtube.py",
    )

    fetch_trends = BashOperator(
        task_id="fetch_trends",
        bash_command=f"cd {PROJECT_DIR} && python scripts/fetch_trends.py",
    )

    format_data = BashOperator(
        task_id="format_data",
        bash_command=f"cd {PROJECT_DIR} && python scripts/format_data.py",
    )

    combine_data = BashOperator(
        task_id="combine_data",
        bash_command=f"cd {PROJECT_DIR} && python scripts/combine_data.py",
    )

    index_elastic = BashOperator(
        task_id="index_elastic",
        bash_command=f"cd {PROJECT_DIR} && python scripts/index_to_elastic.py",
    )

    [fetch_youtube, fetch_trends] >> format_data >> combine_data >> index_elastic

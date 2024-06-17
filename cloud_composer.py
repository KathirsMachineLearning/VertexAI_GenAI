from airflow import models
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with models.DAG(
    'dataflow_model_job',
    default_args=default_args,
    description='A DAG to run a Dataflow job every hour',
    schedule_interval=timedelta(hours=1),
    catchup=False,
) as dag:

    run_dataflow_job = BashOperator(
        task_id='run_dataflow_job',
        bash_command='python3 /home/airflow/gcs/data/model_dataflow.py --region us-central1 --runner DataflowRunner --project fluid-dreamer-423211-s9 --sdk_container_image gcr.io/fluid-dreamer-423211-s9/csa --sdk_location=container',
    )


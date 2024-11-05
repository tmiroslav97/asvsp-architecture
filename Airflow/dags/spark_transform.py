from datetime import datetime


from airflow.decorators import dag, task
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator


@dag(
    dag_id="spark_transform",
    description="DAG in charge of submiting data.",
    start_date=datetime(2024, 11, 5),
    schedule_interval=None,
    max_active_runs=1,
    catchup=False,
)
def spark_transform():

    transform = SparkSubmitOperator(
        task_id='transform',
        conn_id='SPARK_CONNECTION',
        application='/example.py',
        verbose=True
    )

    transform

spark_transform()

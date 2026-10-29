from datetime import datetime

from airflow.providers.apache.hdfs.hooks.webhdfs import WebHDFSHook
from airflow.sdk import dag, task


@dag(
    dag_id="hdfs_load_initial_data",
    description="DAG in charge of submiting data.",
    start_date=datetime(2024, 11, 5),
    schedule=None,
    max_active_runs=1,
    catchup=False,
)
def hdfs_load_initial_data():
    @task
    def load_data():
        hook = WebHDFSHook(webhdfs_conn_id="HDFS_CONNECTION")
        client = hook.get_conn()
        client.makedirs("/data")
        hook.load_file(
            source="/opt/airflow/files/sprogrami2016.csv",
            destination="/data/sprogrami2016.csv",
            overwrite=True,
        )
        return client.list("/data")

    load_data()


hdfs_load_initial_data()

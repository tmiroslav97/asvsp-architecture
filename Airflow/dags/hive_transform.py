from datetime import datetime

from airflow.providers.apache.hive.hooks.hive import HiveServer2Hook
from airflow.sdk import dag, task


@dag(
    dag_id="hive_transform",
    description="DAG in charge of submiting data.",
    start_date=datetime(2024, 11, 5),
    schedule=None,
    max_active_runs=1,
    catchup=False,
)
def hive_transform():

    @task
    def create_table():
        hive_hook = HiveServer2Hook(hiveserver2_conn_id="HIVE_CONNECTION")
        hive_hook.run(
            [
                """
                CREATE EXTERNAL TABLE IF NOT EXISTS programi_source (
                    Id INT,
                    Nazivu STRING,
                    Univerzitet STRING,
                    Naziv STRING,
                    Nivo STRING,
                    Trajanje INT
                )
                ROW FORMAT DELIMITED
                FIELDS TERMINATED BY ','
                LOCATION '/data'
                TBLPROPERTIES ('skip.header.line.count'='1')
                """,
                """
                CREATE TABLE IF NOT EXISTS programi (
                    Id INT,
                    Nazivu STRING,
                    Univerzitet STRING,
                    Naziv STRING,
                    Nivo STRING,
                    Trajanje INT
                )
                ROW FORMAT DELIMITED
                FIELDS TERMINATED BY ','
                """,
            ]
        )

    @task
    def load_data():
        hive_hook = HiveServer2Hook(hiveserver2_conn_id="HIVE_CONNECTION")
        hive_hook.run(
            """
            INSERT OVERWRITE TABLE programi
            SELECT Id, Nazivu, Univerzitet, Naziv, Nivo, Trajanje
            FROM programi_source
            """
        )

    @task
    def query_table():
        hive_hook = HiveServer2Hook(hiveserver2_conn_id="HIVE_CONNECTION")
        print(hive_hook.get_records("SELECT * FROM programi"))

    create_table() >> load_data() >> query_table()


hive_transform()

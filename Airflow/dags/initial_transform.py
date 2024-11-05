from datetime import datetime

from airflow.providers.apache.hive.hooks.hive import HiveServer2Hook
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.providers.ssh.hooks.ssh import SSHHook
from airflow.decorators import dag, task


@dag(
    dag_id="initial_transform",
    description="DAG in charge of submiting data.",
    start_date=datetime(2024, 11, 5),
    schedule_interval=None,
    max_active_runs=1,
    catchup=False,
)
def initial_transform():

    @task
    def create_table():
        hive_hook = HiveServer2Hook(hiveserver2_conn_id="HIVE_CONNECTION")
        # res = hive_hook.get_records("select * from invites")
        # print(res)
        try:
            hive_hook.to_csv(
                "CREATE TABLE programi (Id INT, Nazivu STRING, Univerzitet STRING, Naziv STRING, Nivo STRING, Trajanje INT) row format delimited fields terminated by ',' TBLPROPERTIES('skip.header.line.count'='1')",
                "output.csv",
            )
        except Exception as e:
            print(e)

    @task
    def load_data():
        hive_hook = HiveServer2Hook(hiveserver2_conn_id="HIVE_CONNECTION")
        try:
            hive_hook.to_csv(
                "LOAD DATA INPATH '/data/sprogrami2016.csv' OVERWRITE INTO TABLE programi",
                "output.csv",
            )
        except Exception as e:
            print(e)

    @task
    def describe_table():
        hive_hook = HiveServer2Hook(hiveserver2_conn_id="HIVE_CONNECTION")
        try:
            res = hive_hook.get_records("select * from programi")
            print(res)
        except Exception as e:
            print(e)

    hive_server_ops = SSHOperator(
        task_id="hive_server_task",
        ssh_conn_id="hive_server_ssh_conn",
        command="/opt/hive/bin/beeline -u jdbc:hive2://localhost:10000 -e 'CREATE TABLE pokes2 (foo INT, bar STRING);'",
        cmd_timeout=300,
        ssh_hook=SSHHook(
            remote_host="hive-server",
            username="root",
            password="asvsp",
            banner_timeout=10,
        ),
    )

    create_table() >> load_data() >> describe_table()


initial_transform()

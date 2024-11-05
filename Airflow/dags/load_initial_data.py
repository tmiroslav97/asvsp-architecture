from datetime import datetime

from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.providers.ssh.hooks.ssh import SSHHook

from airflow.decorators import dag


@dag(
    dag_id="load_initial_data",
    description="DAG in charge of submiting data.",
    start_date=datetime(2024, 11, 5),
    schedule_interval=None,
    max_active_runs=1,
    catchup=False,
)
def load_initial_data():
    name_node_ops = SSHOperator(
        task_id="load_data",
        ssh_conn_id="name_node_ssh_conn",
        command="/opt/hadoop-3.2.1/bin/hdfs dfs -mkdir /data && /opt/hadoop-3.2.1/bin/hdfs dfs -copyFromLocal /data/sprogrami2016.csv /data && /opt/hadoop-3.2.1/bin/hdfs dfs -ls /data",
        cmd_timeout=300,
        ssh_hook=SSHHook(
            remote_host="namenode", username="root", password="asvsp", banner_timeout=10
        ),
    )

    name_node_ops


load_initial_data()

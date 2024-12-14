from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum
from datetime import datetime

with DAG(
    dag_id = "dags_bash_operator_test.py",
    start_date=pendulum.datetime(2024, 12, 12, tz = "Asia/Seoul"),
    schedule="30 10 * * *",
    catchup=False
) as dag:

    task1 = BashOperator(
        task_id = "task1",
        bash_command="/opt/airflow/plugins sparktest.sh"
    )
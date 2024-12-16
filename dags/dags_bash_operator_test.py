from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum
from datetime import datetime

file_name = "/opt/airflow/jobs/sparktest.py"

with DAG(
    dag_id = "dags_bash_operator_test",
    start_date=pendulum.datetime(2024, 12, 12, tz = "Asia/Seoul"),
    # 배치일 오전 6시 10분
    schedule="10 6 * * *",
    catchup=False
) as dag:

    task1 = BashOperator(
        task_id = "task1",
        bash_command=f'/opt/airflow/plugins/sparktest.sh {file_name}'
    )
    task1
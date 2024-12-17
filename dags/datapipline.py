from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.models import Variable
import pendulum
from common.get_data import get_data
# params
# api key
api_key = Variable.get("apikey_openapi_nexon")

# DAG
with DAG(
    dag_id = "dags_get_data_python_operator",
    schedule= "0 6 * * *",
    start_date= pendulum.datetime(2024,12,11, tz = "Asia/Seoul"),
    catchup=False
) as dag :

    #[ get_data_task ]
    get_data_ = PythonOperator(
        task_id = "get_data_",
        python_callable=get_data,
        op_args=[api_key]
    )

    #[ data_Refine_task ]
    # sparkjob script
    file_name = "/opt/airflow/jobs/sparktest.py"
    refine_data_ = BashOperator(
        task_id = "refine_data_",
        bash_command=f'/opt/airflow/plugins/sparktest.sh {file_name}'
    )

    # task flow
    get_data_ >> refine_data_
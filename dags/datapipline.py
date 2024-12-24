from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.models import Variable
import pendulum
from common.airflow_common import get_data, check_dir
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

     # [ check_dir_task ] - branch !
    check_dir_ = BranchPythonOperator(
        task_id="check_dir_",
        python_callable=check_dir
    )

    #[ get_data_task ]
    get_today_data_ = PythonOperator(
        task_id = "get_today_data_",
        python_callable=get_data,
        op_args=[api_key,"today"]
    )

    # [ get_yesterday_data_task ]
    get_yesterday_data_ = PythonOperator(
        task_id="get_yesterday_data_",
        python_callable=get_data,
        op_args=[api_key,"yesterday"],
        trigger_rule="none_failed"
    )

    #[ data_refine_task ]
    file_name = "/opt/airflow/jobs/main.py" # sparkjob script
    refine_data_ = BashOperator(
        task_id = "refine_data_",
        bash_command=f'/opt/airflow/plugins/sparktest.sh {file_name}',
        trigger_rule="none_failed"
    )
    
    #[ delete_data_task ]
    delete_data_ = BashOperator(
        task_id ="delete_data_",
        bash_command=" echo 'delete data' "
    )

    # task flow
    check_dir_ >> get_today_data_ >> get_yesterday_data_ >> refine_data_ >> delete_data_
    check_dir_ >> get_today_data_ >> refine_data_ >> delete_data_
    check_dir_ >> get_yesterday_data_ >> refine_data_ >> delete_data_
    check_dir_ >> refine_data_
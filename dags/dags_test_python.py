from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable

import pendulum
import requests
import json
import time
from datetime import datetime

# SET A KEY
api_key = Variable.get("apikey_openapi_nexon")

# DAG
with DAG(
    dag_id = "pro_dags_python_operator_get_data",
    schedule = "0 0 * * *",
    start_date= pendulum.datetime(2024, 12, 11 , tz = "Asia/Seoul"),
    catchup=False
) as dag:
    # GET DATA FUNCTION
    def get_data():
        target_date = datetime.now().strftime("%Y-%m-%d")

        #file_path = f"./data/ranking_{target_date}.json"
    
        headers = {
            "x-nxopen-api-key" : f"{api_key}",
            "User-agent" : "Mozilla/5.0"
            }

        print(f"{target_date} 의 rankingdata 수집을 시작합니다.")
        mydata = []
        for i in range(1,2):
            if i % 20 == 0:
                time.sleep(15)
                url = f"https://open.api.nexon.com/maplestory/v1/ranking/overall?date={target_date}&world_name=%EC%97%98%EB%A6%AC%EC%8B%9C%EC%9B%80&page={i}"
                req = requests.get(url = url, headers = headers)
                data = req.json()
                mydata.append(data)
            else :
                url = f"https://open.api.nexon.com/maplestory/v1/ranking/overall?date={target_date}&world_name=%EC%97%98%EB%A6%AC%EC%8B%9C%EC%9B%80&page={i}"
                req = requests.get(url = url, headers = headers)
                data = req.json()
                mydata.append(data)
    
        #with open(file_path, "w", encoding= "UTF-8-SIG") as f:
        #   json.dump(mydata
        #              ,f
        #              ,ensure_ascii=False
        #            ,indent='\t'
        #            )
            print(mydata)
        return print("done the get ranking job!")
    
    get_data_ = PythonOperator(
        task_id = "get_data_",
        python_callable= get_data
    )

    get_data_
    
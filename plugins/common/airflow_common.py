# [Airflow의 PythonOperator에 전달할 공통함수]

# 수집 전날의 데이터가 제대로 존재하는가 여부를 분기처리 하는 함수
def check_dir(root_dir:str="/opt/airflow/data",**kwargs)->str:
    from pprint import pprint
    from dateutil.relativedelta import relativedelta
    from glob import glob
    # kwargs에 저장된 배치일에서 하루 전날을 계산
    target_date = kwargs["data_interval_end"].in_timezone("Asia/Seoul") + relativedelta(days=-1)
    target_date = target_date.strftime("%Y-%m-%d")
    # 디렉토리에 존재하는 파일 목록을 담을 객체
    data_list = glob(f"ranking_{target_date}.json", root_dir = root_dir )
    # 하루전날 데이터가 존재하지 않는다면
    if not data_list:
        print(f"{target_date}-어제의 데이터가 디렉터리에 존재하지 않습니다.")
        return ["get_yesterday_data","refine_data_","delete_data_"]
    else:
        print(f"{target_date}-어제의 데이터가 디렉터리에 존재합니다!")
        return "refine_data_"

# api 로부터 데이터 수집하는 함수
def get_data(api_key,day:str,**kwargs):
    # schedule 부하 줄이기
    import time
    from dateutil.relativedelta import relativedelta
    import requests
    import json
    from pprint import pprint
    pprint("common fuction의 데이터 수집 함수를 호출합니다.")
    # airflow에서 Batch 시점(data_interval_end)에 한국시간
    # 데이터 수집일 API 호출
    if day == "today":
        target_date = kwargs["data_interval_end"].in_timezone("Asia/Seoul").strftime("%Y-%m-%d")
        # 배치일 6시
        pprint(f"{target_date} 의 rankingdata 호출을 시작합니다.")
    # 데이터 수집 전날 API 호출
    if day == "yesterday":
        target_date = kwargs["data_interval_end"].in_timezone("Asia/Seoul") + relativedelta(days=-1)
        target_date = target_date.strftime("%Y-%m-%d")
    # 호출 헤더
    headers = {
        "x-nxopen-api-key" : f"{api_key}",
        "User-agent" : "Mozilla/5.0"
        }
    # json 파일을 담을 객체
    mydata = []
    # 1페이지당 200명의 랭킹정보
    for i in range(1,2):
        if i % 20 == 0:
            time.sleep(15)
            url = f"https://open.api.nexon.com/maplestory/v1/ranking/overall?date={target_date}&world_name=%EC%97%98%EB%A6%AC%EC%8B%9C%EC%9B%80&page={i}"
            req = requests.get(url = url, headers = headers)
            data = req.json()
            mydata.append(data)
        else:
            url = f"https://open.api.nexon.com/maplestory/v1/ranking/overall?date={target_date}&world_name=%EC%97%98%EB%A6%AC%EC%8B%9C%EC%9B%80&page={i}"
            req = requests.get(url = url, headers = headers)
            data = req.json()
            mydata.append(data)
    pprint(mydata)
    # 호출된 데이터 객체를 data 디렉토리에 저장
    file_path = f"/opt/airflow/data/ranking_{target_date}.json"
    with open (file_path, "w", encoding = "UTF-8-SIG") as f:
        json.dump(mydata,f,ensure_ascii=False,indent='\t')
        print("done")
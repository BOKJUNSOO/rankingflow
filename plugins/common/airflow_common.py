# [Airflow의 PythonOperator에 전달할 공통함수]

# 데이터가 디렉토리에 존재하는가 여부를 분기처리 하는 함수
def check_dir(day:str,root_dir:str="/opt/bitnami/spark/data",**kwargs)->str:
    from dateutil.relativedelta import relativedelta
    from glob import glob

    # BATCH일의 DATA가 수집되어 있는지 확인
    if day == "today":
        batch_date = kwargs["data_interval_end"].in_timezone("Asia/Seoul").strftime("%Y-%m-%d")
        print(f"{batch_date}의 데이터가 존재하는지 확인합니다.")
        data_list = glob(f"ranking_{batch_date}.json",root_dir = root_dir)

        # BATCH일의 DATA가 없다면
        if not data_list:
            print(f"{batch_date}일자의 데이터가 존재하지 않습니다.")
            # BATCH일의 DATA를 수집하는 TASK를 실행
            next_task = "get_today_data_"
        else:
            print(f"{batch_date}일자의 데이터가 존재합니다.")
            next_task = "check_yesterday_data_"

    # BATCH 전날의 DATA가 수집되어 있는지 확인
    if day == "yesterday":
        before_batch_date = kwargs["data_interval_end"].in_timezone("Asia/Seoul") + relativedelta(days=-1)
        before_batch_date = before_batch_date.strftime("%Y-%m-%d")
        print(f"{before_batch_date}의 데이터가 존재하는지 확인합니다.")
        data_list = glob(f"ranking_{before_batch_date}.json", root_dir = root_dir )

        # BATCH일의 DATA가 없다면
        if not data_list:
            print(f"{before_batch_date}일자의 데이터가 존재하지 않습니다.")
            # BATCH전날의 DATA를 수집하는 TASK를 실행
            next_task = "get_yesterday_data_"
        else:
            print(f"{before_batch_date}일자의 데이터가 존재합니다.")
            next_task = "check_data_quality_"
    return next_task
    

# api 로부터 데이터 수집하는 함수
def get_data(api_key,day:str,**kwargs):
    # schedule 부하 줄이기
    import time
    from dateutil.relativedelta import relativedelta
    import requests
    import json
    print("common fuction의 데이터 수집 함수를 호출합니다.")

    # 데이터 수집일 API 호출
    if day == "today":
        target_date = kwargs["data_interval_end"].in_timezone("Asia/Seoul").strftime("%Y-%m-%d")
        # 배치일 6시
        print(f"{target_date} 의 rankingdata 호출을 시작합니다.")
    
    # 데이터 수집 전날 API 호출
    if day == "yesterday":
        target_date = kwargs["data_interval_end"].in_timezone("Asia/Seoul") + relativedelta(days=-1)
        target_date = target_date.strftime("%Y-%m-%d")
        print(f"{target_date} 의 rankingdata 호출을 시작합니다.")
    # 호출 헤더
    headers = {
        "x-nxopen-api-key" : f"{api_key}",
        "User-agent" : "Mozilla/5.0"
        }
    # json 파일을 담을 객체
    mydata = []

    # 1페이지당 200명의 랭킹정보
    for i in range(1,300):
        if i % 50 == 0:
            time.sleep(15)
        if i % 20 == 0:
            print(f"{i}번째 페이지를 호출중입니다.")
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
    
    print("ranking_data 호출이 끝났습니다.")
    
    # 호출된 데이터 객체를 data 디렉토리에 저장
    file_path = f"/opt/bitnami/spark/data/{target_date}.json"
    with open (file_path, "w", encoding = "UTF-8-SIG") as f:
        json.dump(mydata,f,ensure_ascii=False,indent='\t')
        print("done")
    return
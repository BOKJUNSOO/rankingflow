`Airflow` Project Repo (with `Spark` and `Nexon Open API`)

# ETL 아키텍쳐
<img src="./README_IMG/ETL아키텍쳐.jpg" alt="아키텍쳐 다이어그램" width="200%"/>

# 프로젝트 시작하기
### 📥 프로젝트 클론하기
```bash
git clone https://github.com/BOKJUNSOO/rankingflow.git
```

### 🐋 도커엔진 다운로드하기

#### 1. 설치전 실행

```bash
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```
- set up

```bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

#### 2. 도커 패키지 다운로드
```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

#### 3. 도커엔진 실행
```bash
sudo service docker start
```

### 📦 container 빌드

```bash
sudo docker compose up --build -d
```

### 🗝️ Nexon Api Key 발급받고 입력하기
- 사이트에 접속해서 API키를 발급받아주세요.
> https://openapi.nexon.com/ko/

- localhost:8081로 접속합니다.

- 상단의 Admin > Variables로 들어갑니다.
<img src="./README_IMG/airflowkey1.png" alt="key등록1">

- `+` 버튼을 눌러 키를 추가해줍니다
   - `Key` 부분에 `apikey_openapi_nexon`을 입력하고
   - `Val` 부분에 발급받은 키를 입력합니다.

### ▶️ Project Start
- `datapipline` `dags`를 `unpause` 시켜주세요.
- localhost:5601로 접속하여 `kibana`를 이용한 데이터 시각화가 가능합니다.
   - `Dashboard`
   - 최초 저장되는 데이터를 기준으로 
   좌측에 메뉴에서 `Discover`으로 `Create a data view`를 필요로 합니다.
<img src="./README_IMG/kibana.png" alt="kibana 페이지">



FROM apache/airflow:2.10.3

# 사용자 변경
USER root

# Spark 3.5.1 설치 및 OpenJDK 17 설치
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         openjdk-17-jre-headless \
         wget \
  && wget https://downloads.apache.org/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz -O /tmp/spark-3.5.1-bin-hadoop3.tgz \
  && tar xvf /tmp/spark-3.5.1-bin-hadoop3.tgz -C /opt/ \
  && rm /tmp/spark-3.5.1-bin-hadoop3.tgz \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# 환경 변수 설정
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV SPARK_HOME=/opt/spark-3.5.1-bin-hadoop3
ENV PATH=$SPARK_HOME/bin:$PATH

# airflow 사용자로 돌아가기
USER airflow

# Airflow 및 SparkProvider 설치
RUN pip install --no-cache-dir \
    "apache-airflow==${AIRFLOW_VERSION}" \
    apache-airflow-providers-apache-spark




FROM apache/airflow:2.10.3

USER root

# 필요한 패키지 설치
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         openjdk-17-jre-headless \
         wget \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Spark 3.5.1 설치
RUN wget https://archive.apache.org/dist/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.2.tgz \
  && tar xvf spark-3.5.1-bin-hadoop3.2.tgz \
  && mv spark-3.5.1-bin-hadoop3.2 /opt/spark

# 환경 변수 설정
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH

USER airflow

# Airflow와 PySpark, Spark provider 버전 맞추기
RUN pip install --no-cache-dir \
  "apache-airflow==2.10.3" \
  "apache-airflow-providers-apache-spark==2.5.0" \
  "pyspark==3.5.1" \
  elasticsearch

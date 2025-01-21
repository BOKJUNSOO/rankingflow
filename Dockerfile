FROM apache/airflow:2.10.3

# Spark 3.5.1 설치
USER root
RUN apt-get update \
  && apt-get install -y wget openjdk-17-jre-headless \
  && wget -q https://archive.apache.org/dist/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.3.tgz \
  && tar -xvzf spark-3.5.1-bin-hadoop3.3.tgz -C /opt/ \
  && rm spark-3.5.1-bin-hadoop3.3.tgz

# 환경 변수 설정
ENV SPARK_HOME=/opt/spark-3.5.1-bin-hadoop3.3
ENV PATH=$SPARK_HOME/bin:$PATH
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# 추가적으로 필요한 Python 라이브러리 설치
USER airflow
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" apache-airflow-providers-apache-spark pyspark elasticsearch


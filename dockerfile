FROM apache/airflow:2.10.3-python3.12

# Spark 설치
ENV SPARK_VERSION=3.4.1

RUN apt-get update && \
    apt-get install -y openjdk-11-jdk curl && \
    curl -O https://downloads.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz && \
    tar -xzf spark-${SPARK_VERSION}-bin-hadoop3.tgz -C /opt && \
    ln -s /opt/spark-${SPARK_VERSION}-bin-hadoop3 /opt/spark && \
    rm spark-${SPARK_VERSION}-bin-hadoop3.tgz

# 환경 변수 설정
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH
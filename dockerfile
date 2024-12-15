#Dockerfile
FROM apache/airflow:2.10.3-python3.12

USER root
RUN apt-get update && \
    apt-get install -y gcc python3-dev openjdk-11-jdk && \
    apt-get clean

# Set JAVA_HOME environment variable
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-arm64

USER airflow

RUN pip install apache-airflow apache-airflow-providers-apache-spark pyspark
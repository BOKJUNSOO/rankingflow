FROM apache/airflow:2.10.3-python3.12

USER root
RUN apt-get update
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    openjdk-11-jdk \
    wget
RUN apt-get clean

# Set JAVA_HOME environment variable
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-arm64

USER airflow

RUN pip install apache-airflow==2.7.1 apache-airflow-providers-apache-spark pyspark elasticsearch numpy requests
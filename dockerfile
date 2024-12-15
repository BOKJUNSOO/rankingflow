FROM apache/airflow:2.10.3-python3.9

USER root
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get clean;

# Set JAVA_HOME environment variable
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-arm64
RUN export JAVA_HOME

USER airflow
RUN pip install --upgrade apache-airflow-providers-openlineage>=1.8.0 apache-airflow-providers-apache-spark pyspark


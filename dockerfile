FROM apache/airflow:2.10.3
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

USER airflow
RUN pip install --upgrade apache-airflow-providers-openlineage>=1.8.0 apache-airflow-providers-apache-spark pyspark


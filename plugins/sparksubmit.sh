#!/bin/bash

script=$@
JOBNAME="RefineData"
DRIVER_MEMORY="2g"
EXECUTOR_MEMORY="4g"
echo "Job name is ${JOBNAME}"
echo "submit this job >> ${script}"
echo 'start spark submit with bash operator'

spark-submit \
    --name ${JOBNAME} \
    --jars /opt/airflow/resources/elasticsearch-spark-30_2.12-8.11.1.jar,/opt/airflow/resources/mysql-connector-j-8.0.33.jar \
    --master spark://spark-master:7077 ${script} \
    --conf spark.driver.memory=${DRIVER_MEMORY} \
    --conf spark.executor.memory=${EXECUTOR_MEMORY} \
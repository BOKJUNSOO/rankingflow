#!/bin/bash

script=$@
JOBNAME="RefineData"
echo "Job name is ${JOBNAME}"
echo "submit this job >> ${script}"
echo 'start spark submit with bash operator'

spark-submit \
    --name ${JOBNAME} \
    --jars /opt/airflow/resources/elasticsearch-spark-30_2.12-7.15.2.jar \
    --master spark://spark-master:7077 ${script}
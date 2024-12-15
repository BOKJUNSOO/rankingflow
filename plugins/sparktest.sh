#!/bin/bash

script=$1
JOBNAME=$JOBNAME
echo "${script}"
echo "start spark submit with bash operator"

spark-submit \
    --name ${JOBNAME} \
    --master spark://spark-master:7077 \
    ${script}   # /opt/airflow/jobs/pyfile
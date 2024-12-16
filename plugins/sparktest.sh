#!/bin/bash

script=$1
JOBNAME="RefineData"
echo "Job name is $JOBNAME"
echo "submit this job >> ${script}"
echo "start spark submit with bash operator"

spark-submit \
    --name ${JOBNAME} \
    --master spark://spark-master:7077 ${script}
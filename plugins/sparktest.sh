#!/bin/bash

script=$1
echo "${script}"
echo "start spark submit with bash operator"
echo "${PATH}"
echo "${SPARK_HOME}"
docker exec -it rankingflow-spark-master-1 spark-submit --master spark://spark-master:7077 ${script}
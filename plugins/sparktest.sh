#!/bin/bash

script=$1
echo "${script}"
echo "start spark submit with bash operator"
echo "${PATH}"
echo "${SPARK_HOME}"
spark-submit \
    --master spark://spark-master:7077 ${script}
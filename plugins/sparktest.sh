#!/bin/bash

script=$1
echo "${script}"
echo "start spark submit with bash operator"

spark-submit \
    --master spark://spark-master:7077 jobs/${script}
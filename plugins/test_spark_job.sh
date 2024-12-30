#!/bin/bash

script=$@

docker exec -it rankingflow-spark-master-1 spark-submit \
    --master spark://spark-master:7077 ${script} \
    --conf spark.eventLog.enabled=true
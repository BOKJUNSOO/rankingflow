#!/bin/bash

script=$1

docker exec -it rankingflow-spark-master-1 spark-submit \
        --master spark://spark-master:7077 jobs/${script}
#!/bin/bash

index=$1
date=$2

echo "저장된 인덱스 목록"
curl -X GET "localhost:9200/_cat/indices?pretty"

echo
echo "${index}_${date}저장된 데이터"
curl -X GET "localhost:9200/${index}_${date}_search?pretty"
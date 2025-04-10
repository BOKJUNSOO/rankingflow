#!/bin/bash

index=$1

echo "저장된 인덱스 목록"
curl -X GET "localhost:9200/_cat/indices?pretty"

echo
echo "${index} 의 사냥 데이터"
curl -X GET "http://localhost:9200/user_exp_*/_search?pretty" \
	     -H 'Content-Type: application/json' \
	          -d @- <<EOF
{
  "query": {
    "match": {
      "character_name": "${index}"
    }
  }
}
EOF

#!/bin/bash
today_date=$1
yesterday_date=$2
echo "${today_date}의 데이터 누락여부를 확인합니다."
cat ./data/ranking_${today_date} | grep 'please'
if [ $? -eq 1]; then
    echo "${today_date}의 누락된 데이터가 존재합니다."
else
    echo "${today_date}의 누락된 데이터가 존재하지 않습니다."
fi

echo "${yesterday_date}의 데이터 누락여부를 확인합니다."
cat ./data/ranking_${yesterday_date} | grep 'please'
if [ $? -eq 1]; then
    echo "${yesterday_date}의 누락된 데이터가 존재합니다."
else
    echo "${yesterday_date}의 누락된 데이터가 존재하지 않습니다."
fi
#!/bin/sh

start_date=$1
interval=10

if [ $# -gt 2 ];then
  interval=$3
fi

filename=1
rm -f ./data/*

while [ $start_date -lt $2 ]; do
  end_date=`date -d "${interval} days ${start_date}" +%Y%m%d`
  if [ ${end_date} -gt $2 ]; then
    end_date=$2
  fi

  echo "hive -hiveconf start_date=${start_date} -hiveconf end_date=${end_date} -f etl_deliver.hql > ./data/${filename}"

  hive -hiveconf start_date=${start_date} -hiveconf end_date=${end_date} -f etl_deliver.hql > ./data/${filename}
  filename=$((filename+1))
  start_date=`date -d "1 days ${end_date}" +%Y%m%d`
done

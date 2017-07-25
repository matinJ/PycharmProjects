#!/bin/sh

cd `dirname $0`

if [ $# -gt 2 ]; then
  start_date=$1
  end_date=$2
else
  start_date=`date -d '100 days ago' +%Y%m%d`
  end_date=`date -d '2 days ago' +%Y%m%d`
fi
date=`date -d 'yesterday' +%Y%m%d`
filename=0

cc=`hive -e "select count(1) from uf20.exchangedate where exchange_type=1 and init_date=${date}"`
echo "cc: ${cc}"
if [ "${cc}" -lt 1 ]; then
  echo "${date} is not an exchange date."
  exit 0
fi

#历史购买情况
echo "hive -hiveconf start_date=${start_date} -hiveconf end_date=${end_date} -f etl_buy.hql > ./data/${filename}"
hive -hiveconf start_date=${start_date} -hiveconf end_date=${end_date} -f etl_buy.hql > ./data/${filename}

python buy_cluster.py ./data/${filename}

#用户的分类信息
mysql -h192.1.3.131 -ubeehivehty131 -pbeehive@131.fzsc -Dstat -e "truncate table t_client_cluster"
mysql -h192.1.3.131 -ubeehivehty131 -pbeehive@131.fzsc -Dstat -e "load data local infile '/opt/applications/script/machine_learning/clustering.r' into table t_client_cluster (client_id, label)"

#用户的股票信息
mysql -h192.1.3.131 -ubeehivehty131 -pbeehive@131.fzsc -Dstat -e "truncate table t_client_stock"
mysql -h192.1.3.131 -ubeehivehty131 -pbeehive@131.fzsc -Dstat -e "load data local infile '/opt/applications/script/machine_learning/data/0' into table t_client_stock (client_id, stock_code, amount, stock_name)"

#昨天的购买情况
hive -hiveconf date=${date} -f yesterday_buy.hql > ./data/yesterday

#recommendation
python recommendations.py clustering.r  ./data/yesterday
mysql -h192.1.3.131 -ubeehivehty131 -pbeehive@131.fzsc -Dstat -e "truncate table t_client_recommendation"
mysql -h192.1.3.131 -ubeehivehty131 -pbeehive@131.fzsc -Dstat -e "load data local infile '/opt/applications/script/machine_learning/recommendations.r' into table t_client_recommendation (client_id, stock_code,stock_name)"

#!/bin/bash

PROJ_HOME=/home/hdp-dianshang/jinxueyu
hadoop jar /home/hdp-dianshang/software/hadoop-fb-0.20.1.9-streaming.jar \
    -files $PROJ_HOME/bigger/src/main/py/    \
    -mapper "python2.6 py/classification/stat/stat_cat_data_job.py price map"  \
    -combiner "python2.6 py/classification/stat/stat_cat_data_job.py price reduce" \
    -reducer "python2.6 py/classification/stat/stat_cat_data_job.py price reduce" \
    -numReduceTasks 128 \
    -input /home/hdp-dianshang/jinxueyu/goods_snapshot/20150410/ \
    -output /home/hdp-dianshang/jinxueyu/stat/price/20150410 \
    -jobconf mapred.job.name=jinxueyu_stat_job
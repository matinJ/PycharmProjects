#!/bin/bash

PROJ_HOME=/home/hdp-dianshang/jinxueyu
hadoop jar /home/hdp-dianshang/software/hadoop-fb-0.20.1.9-streaming.jar \
    -files $PROJ_HOME/bigger/src/main/py/    \
    -mapper "python2.6 py/classification/goods_classifier/select_training_data_job.py map"  \
    -reducer "python2.6 py/classification/goods_classifier/select_training_data_job.py reduce" \
    -numReduceTasks 128 \
    -input /home/hdp-dianshang/data/qihoo-mall-goodsinfo/callback.log/20150410/ \
    -output /home/hdp-dianshang/jinxueyu/goods_snapshot/20150410 \
    -jobconf mapred.job.name=jinxueyu_format_cf_log
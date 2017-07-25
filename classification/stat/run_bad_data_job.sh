#!/bin/bash

PROJ_HOME=/home/hdp-dianshang/jinxueyu
hadoop jar /home/hdp-dianshang/software/hadoop-fb-0.20.1.9-streaming.jar \
    -files $PROJ_HOME/bigger/src/main/py/    \
    -mapper "python2.6 py/classification/stat/select_bad_data_job.py map"  \
    -reducer "python2.6 py/classification/stat/select_bad_data_job.py reduce" \
    -numReduceTasks 128 \
    -input /home/hdp-dianshang/data/qihoo-mall-goodsinfo/callback.log/ \
    -output /home/hdp-dianshang/jinxueyu/baddata/ \
    -jobconf mapred.job.name=jinxueyu_bad_job
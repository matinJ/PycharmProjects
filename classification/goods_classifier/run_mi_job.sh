#!/bin/bash

PROJ_HOME=/home/hdp-dianshang/jinxueyu
hadoop jar /home/hdp-dianshang/software/hadoop-fb-0.20.1.9-streaming.jar \
    -files $PROJ_HOME/bigger/src/main/py/    \
    -mapper "python2.6 py/classification/goods_classifier/mi_job.py map"  \
    -reducer "python2.6 py/classification/goods_classifier/mi_job.py reduce" \
    -numReduceTasks 128 \
    -input /home/hdp-dianshang/jinxueyu/goods_feature/20150410/ \
    -output /home/hdp-dianshang/jinxueyu/model/20150410 \
    -jobconf mapred.job.name=jinxueyu_mi_job
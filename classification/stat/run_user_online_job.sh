#!/bin/bash

PROJ_HOME=/home/hdp-dianshang/jinxueyu
hadoop jar /home/hdp-dianshang/software/hadoop-fb-0.20.1.9-streaming.jar \
    -files $PROJ_HOME/bigger/src/main/py/    \
    -mapper "python2.6 py/classification/stat/stat_user_online_job.py map"  \
    -reducer "python2.6 py/classification/stat/stat_user_online_job.py reduce" \
    -numReduceTasks 128 \
    -input /home/hdp-dianshang/log/callback/20150604 \
    -output /home/hdp-dianshang/jinxueyu/stat_user_log/ \
    -jobconf mapred.job.name=jinxueyu_user_job
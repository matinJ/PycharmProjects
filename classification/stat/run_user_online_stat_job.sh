#!/bin/bash

PROJ_HOME=/home/hdp-dianshang/jinxueyu
hadoop jar /home/hdp-dianshang/software/hadoop-fb-0.20.1.9-streaming.jar \
    -files $PROJ_HOME/bigger/src/main/py/    \
    -mapper "python2.6 py/classification/stat/stat_user_online_job.py stat_map"  \
    -combiner "python2.6 py/classification/stat/stat_user_online_job.py stat_reduce" \
    -reducer "python2.6 py/classification/stat/stat_user_online_job.py stat_reduce" \
    -numReduceTasks 1 \
    -input /home/hdp-dianshang/jinxueyu/stat_user_log/ \
    -output /home/hdp-dianshang/jinxueyu/stat_user_time/ \
    -jobconf mapred.job.name=jinxueyu_stat_user_job
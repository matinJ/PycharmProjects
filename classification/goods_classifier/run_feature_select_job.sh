#!/bin/bash

PROJ_HOME=/home/hdp-dianshang/jinxueyu
hadoop jar /home/hdp-dianshang/software/hadoop-fb-0.20.1.9-streaming.jar \
    -files $PROJ_HOME/bigger/src/main/py/    \
    -mapper "python2.6 py/classification/goods_classifier/feature_selection_job.py ppmap"  \
    -combiner "python2.6 py/classification/goods_classifier/feature_selection_job.py ppreduce" \
    -reducer "python2.6 py/classification/goods_classifier/feature_selection_job.py ppreduce" \
    -numReduceTasks 1 \
    -input /home/hdp-dianshang/jinxueyu/goods_feature/20150410/ \
    -output /home/hdp-dianshang/jinxueyu/goods_feature_catinfo/20150410 \
    -jobconf mapred.job.name=jinxueyu_feature_ig_job

hadoop dfs -cat /home/hdp-dianshang/jinxueyu/goods_feature_catinfo/20150410/* > $PROJ_HOME/bigger/src/main/py/classification/goods_classifier/cat_info
# get cat count file, add in the program

PROJ_HOME=/home/hdp-dianshang/jinxueyu
hadoop jar /home/hdp-dianshang/software/hadoop-fb-0.20.1.9-streaming.jar \
    -files $PROJ_HOME/bigger/src/main/py/    \
    -mapper "python2.6 py/classification/goods_classifier/feature_selection_job.py igmap"  \
    -reducer "python2.6 py/classification/goods_classifier/feature_selection_job.py igreduce" \
    -numReduceTasks 128 \
    -input /home/hdp-dianshang/jinxueyu/goods_feature/20150410/ \
    -output /home/hdp-dianshang/jinxueyu/goods_feature_selection/20150410 \
    -jobconf mapred.job.name=jinxueyu_feature_ig_job
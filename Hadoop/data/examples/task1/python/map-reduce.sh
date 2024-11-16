#!/bin/bash
DIR=/zadatak1

cd $DIR

hdfs dfs -rm -r -f /mean_out_py

printf "\nSETTING EXECUTEABLE PY\n"

chmod a+x *.py

cd $HADOOP_PREFIX

printf "\nRUN HADOOP-STREAMING\n"

mapred streaming \
    -input /mean \
    -output /mean_out_py \
    -mapper mapper.py \
    -reducer reducer.py \
    -file $DIR/mapper.py \
    -file $DIR/reducer.py

printf "\nRESULTS\n"

hdfs dfs -cat /mean_out_py/* | $DIR/mean.py
#!/bin/bash
DIR=/zadatak3

cd $DIR

hdfs dfs -rm -r -f /friends_out_py

printf "\nSETTING EXECUTEABLE PY\n"

chmod a+x *.py

cd $HADOOP_PREFIX

printf "\nRUN HADOOP-STREAMING\n"

mapred streaming \
    -input /friends \
    -output /friends_out_py \
    -mapper mapper.py \
    -reducer reducer.py \
    -file $DIR/mapper.py \
    -file $DIR/reducer.py

printf "\nRESULTS\n"

hdfs dfs -cat /friends_out_py/*
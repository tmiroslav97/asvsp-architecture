#!/bin/bash
DIR1=/zadatak1

cd $DIR1

hdfs dfs -rm -r -f /var_mean_py

printf "\nSETTING EXECUTEABLE PY\n"

chmod a+x *.py

cd $HADOOP_PREFIX

printf "\nRUN HADOOP-STREAMING\n"

mapred streaming \
    -input /mean \
    -output /var_mean_py \
    -mapper mapper.py \
    -reducer reducer.py \
    -file $DIR1/mapper.py \
    -file $DIR1/reducer.py

MEAN=$(hdfs dfs -cat /var_mean_py/* | $DIR1/mean.py)

DIR2=/zadatak2
cd $DIR2

hdfs dfs -rm -r -f /var_out_py

printf "\nSETTING EXECUTEABLE PY\n"
chmod a+x *.py

cd $HADOOP_PREFIX

printf "\nRUN HADOOP-STREAMING\n"
mapred streaming \
    -input /mean \
    -output /var_out_py \
    -mapper mapper.py \
    -reducer reducer.py \
    -file $DIR2/mapper.py \
    -file $DIR1/reducer.py \
    -cmdenv MEAN=$MEAN

printf "\nRESULTS\n"
hdfs dfs -cat /var_out_py/*
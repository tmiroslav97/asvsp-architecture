#!/bin/bash

DIR=/shpth

cd $DIR

printf "\nCOPY FILE TO HDFS\n"

hdfs dfs -rm -r -f /shpth_1/

hdfs dfs -mkdir /shpth_1/
hdfs dfs -put data.txt /shpth_1

printf "\nSETTING EXECUTEABLE PY\n"

chmod a+x *.py

cd $HADOOP_PREFIX

for i in 1 2 3 4
do
    hdfs dfs -rm -r -f "/shpth_$(($i+1))/"

    printf "\nRUN HADOOP-STREAMING\n"

    mapred streaming \
        -input "/shpth_$i/" \
        -output "/shpth_$(($i+1))/" \
        -mapper mapper.py \
        -reducer reducer.py \
        -file $DIR/mapper.py \
        -file $DIR/reducer.py > /dev/null

    printf "\nRESULTS $i\n"

    hdfs dfs -cat "/shpth_$(($i+1))/*"
done
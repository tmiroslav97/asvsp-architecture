#!/bin/bash
DIR=/example3

cd $DIR

printf "\nCOPY FILE TO HDFS\n"

hdfs dfs -put dq.txt /book

printf "\nSETTING EXECUTEABLE PY\n"

chmod a+x *.py

cd $HADOOP_HOME

printf "\nRUN HADOOP-STREAMING\n"

mapred streaming \
    -input /book \
    -output /book_out \
    -mapper mapper.py \
    -reducer reducer.py \
    -file $DIR/mapper.py \
    -file $DIR/reducer.py

printf "\nRESULTS\n"

hdfs dfs -cat /book_out/*
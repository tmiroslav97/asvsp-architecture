#!/bin/bash
set -euo pipefail

DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
HADOOP_HOME="${HADOOP_HOME:-${HADOOP_PREFIX:-$(cd "$(dirname "$(command -v hadoop)")/.." && pwd)}}"
STREAMING_JAR=$(find "$HADOOP_HOME/share/hadoop/tools/lib" -maxdepth 1 -name 'hadoop-streaming-*.jar' -print -quit)
: "${STREAMING_JAR:?Hadoop Streaming JAR not found}"

cd "$DIR"

printf "\nCOPY FILE TO HDFS\n"

hdfs dfs -rm -r -f /book
hdfs dfs -put dq.txt /book

printf "\nSETTING EXECUTEABLE PY\n"

chmod a+x *.py

printf "\nRUN HADOOP-STREAMING\n"

hadoop jar "$STREAMING_JAR" \
    -input /book \
    -output /book_out \
    -file "$DIR/mapper.py" \
    -file "$DIR/reducer.py" \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py"

printf "\nRESULTS\n"

hdfs dfs -cat /book_out/*

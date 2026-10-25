#!/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
DIR1="$SCRIPT_DIR"
HADOOP_HOME="${HADOOP_HOME:-${HADOOP_PREFIX:-$(cd "$(dirname "$(command -v hadoop)")/.." && pwd)}}"
STREAMING_JAR=$(find "$HADOOP_HOME/share/hadoop/tools/lib" -maxdepth 1 -name 'hadoop-streaming-*.jar' -print -quit)
: "${STREAMING_JAR:?Hadoop Streaming JAR not found}"

cd "$DIR1"

hdfs dfs -rm -r -f /var_mean_py

printf "\nSETTING EXECUTEABLE PY\n"

chmod a+x *.py

printf "\nRUN HADOOP-STREAMING\n"

hadoop jar "$STREAMING_JAR" \
    -input /mean \
    -output /var_mean_py \
    -file "$DIR1/mean_mapper.py" \
    -file "$DIR1/reducer.py" \
    -mapper "python3 mean_mapper.py" \
    -reducer "python3 reducer.py"

MEAN=$(hdfs dfs -cat /var_mean_py/* | python3 "$DIR1/mean.py")

DIR2="$SCRIPT_DIR"
cd "$DIR2"

hdfs dfs -rm -r -f /var_out_py

printf "\nSETTING EXECUTEABLE PY\n"
chmod a+x *.py

printf "\nRUN HADOOP-STREAMING\n"
hadoop jar "$STREAMING_JAR" \
    -input /mean \
    -output /var_out_py \
    -file "$DIR2/mapper.py" \
    -file "$DIR2/reducer.py" \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -cmdenv MEAN=$MEAN

printf "\nRESULTS\n"
hdfs dfs -cat /var_out_py/*

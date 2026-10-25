#!/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TASK_DIR=$(cd "$SCRIPT_DIR/.." && pwd)
DIR="$SCRIPT_DIR"
HADOOP_HOME="${HADOOP_HOME:-${HADOOP_PREFIX:-$(cd "$(dirname "$(command -v hadoop)")/.." && pwd)}}"
STREAMING_JAR=$(find "$HADOOP_HOME/share/hadoop/tools/lib" -maxdepth 1 -name 'hadoop-streaming-*.jar' -print -quit)
: "${STREAMING_JAR:?Hadoop Streaming JAR not found}"

cd "$DIR"

hdfs dfs -rm -r -f /mean_out_py
hdfs dfs -rm -r -f /mean
if [[ ! -f "$TASK_DIR/sample.csv" ]]; then
    (cd "$TASK_DIR" && python3 generate-file.py)
fi
hdfs dfs -put "$TASK_DIR/sample.csv" /mean

printf "\nSETTING EXECUTEABLE PY\n"

chmod a+x *.py

printf "\nRUN HADOOP-STREAMING\n"

hadoop jar "$STREAMING_JAR" \
    -input /mean \
    -output /mean_out_py \
    -file "$DIR/mapper.py" \
    -file "$DIR/reducer.py" \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py"

printf "\nRESULTS\n"

hdfs dfs -cat /mean_out_py/* | python3 "$DIR/mean.py"

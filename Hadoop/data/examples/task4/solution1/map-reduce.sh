#!/bin/bash
set -euo pipefail

DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
HADOOP_HOME="${HADOOP_HOME:-${HADOOP_PREFIX:-$(cd "$(dirname "$(command -v hadoop)")/.." && pwd)}}"
STREAMING_JAR=$(find "$HADOOP_HOME/share/hadoop/tools/lib" -maxdepth 1 -name 'hadoop-streaming-*.jar' -print -quit)
: "${STREAMING_JAR:?Hadoop Streaming JAR not found}"

cd "$DIR"

if ! hdfs dfs -test -e /cross; then
    echo "Missing HDFS input: /cross. Upload a text file first: hdfs dfs -put <file> /cross" >&2
    exit 1
fi

hdfs dfs -rm -r -f /cross_out_py

printf "\nSETTING EXECUTEABLE PY\n"

chmod a+x *.py

printf "\nRUN HADOOP-STREAMING\n"

hadoop jar "$STREAMING_JAR" \
    -input /cross \
    -output /cross_out_py \
    -file "$DIR/mapper.py" \
    -file "$DIR/reducer.py" \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py"

printf "\nRESULTS\n"

# hdfs dfs -cat /cross_out_py/*

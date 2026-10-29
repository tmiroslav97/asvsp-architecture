#!/bin/bash
set -euo pipefail

DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
HADOOP_HOME="${HADOOP_HOME:-${HADOOP_PREFIX:-$(cd "$(dirname "$(command -v hadoop)")/.." && pwd)}}"
STREAMING_JAR=$(find "$HADOOP_HOME/share/hadoop/tools/lib" -maxdepth 1 -name 'hadoop-streaming-*.jar' -print -quit)
: "${STREAMING_JAR:?Hadoop Streaming JAR not found}"

cd "$DIR"

printf "\nCOPY FILE TO HDFS\n"

hdfs dfs -rm -r -f /shpth_1/

hdfs dfs -mkdir /shpth_1/
hdfs dfs -put data.txt /shpth_1

printf "\nSETTING EXECUTEABLE PY\n"

chmod a+x *.py

for i in 1 2 3 4
do
    hdfs dfs -rm -r -f "/shpth_$(($i+1))/"

    printf "\nRUN HADOOP-STREAMING\n"

    hadoop jar "$STREAMING_JAR" \
        -input "/shpth_$i/" \
        -output "/shpth_$(($i+1))/" \
        -file "$DIR/mapper.py" \
        -file "$DIR/reducer.py" \
        -mapper "python3 mapper.py" \
        -reducer "python3 reducer.py" > /dev/null

    printf "\nRESULTS $i\n"

    hdfs dfs -cat "/shpth_$(($i+1))/*"
done

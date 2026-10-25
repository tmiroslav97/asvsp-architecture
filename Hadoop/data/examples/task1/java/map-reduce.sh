#!/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TASK_DIR=$(cd "$SCRIPT_DIR/.." && pwd)
cd "$SCRIPT_DIR"

hdfs dfs -rm -r -f /mean
hdfs dfs -rm -r -f /mean_out_j
if [[ ! -f "$TASK_DIR/sample.csv" ]]; then
    (cd "$TASK_DIR" && python3 generate-file.py)
fi
hdfs dfs -put "$TASK_DIR/sample.csv" /mean

printf "\nSET CLASSPATHS\n"

HADOOP_HOME="${HADOOP_HOME:-${HADOOP_PREFIX:-$(cd "$(dirname "$(command -v hadoop)")/.." && pwd)}}"

printf "\nCOMPILE JAVA\n"

rm -rf build
mkdir build
javac -cp "$(hadoop classpath --glob)" -d build CalculateMean.java

printf "\nBUILD JAR\n"

jar cfm CalculateMean.jar Manifest.txt -C build .

printf "\nRUN MAP-REDUCE\n"

hadoop jar CalculateMean.jar CalculateMean /mean /mean_out_j

printf "\nRESULTS\n"

hdfs dfs -cat /mean_out_j/*

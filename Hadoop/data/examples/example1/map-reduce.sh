#!/bin/bash
set -euo pipefail

cd /example1

printf "\nCOPY FILE TO HDFS\n"

hdfs dfs -rm -r -f /units
hdfs dfs -put sample.txt /units

printf "\nSET CLASSPATHS\n"

HADOOP_HOME="${HADOOP_HOME:-${HADOOP_PREFIX:-$(cd "$(dirname "$(command -v hadoop)")/.." && pwd)}}"

printf "\nCOMPILE JAVA\n"

rm -rf build
mkdir build
javac -cp "$(hadoop classpath --glob)" -d build ProcessUnits.java

printf "\nBUILD JAR\n"

jar cfm ProcessUnits.jar Manifest.txt -C build .

printf "\nRUN MAP-REDUCE\n"

hadoop jar ProcessUnits.jar ProcessUnits /units /units_out

printf "\nRESULTS\n"

hdfs dfs -cat /units_out/*

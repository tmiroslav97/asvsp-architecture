#!/bin/bash
set -euo pipefail

cd /opt/hadoop/example2

printf "\nCOPY FILE TO HDFS\n"

hdfs dfs -rm -r -f /sales_out/
hdfs dfs -rm -r -f /sales
hdfs dfs -put SalesJan2009.csv /sales

printf "\nSET CLASSPATHS\n"

HADOOP_HOME="${HADOOP_HOME:-${HADOOP_PREFIX:-$(cd "$(dirname "$(command -v hadoop)")/.." && pwd)}}"

printf "\nCOMPILE JAVA\n"

rm -rf build
mkdir build
javac -cp "$(hadoop classpath --glob)" -d build src/*.java

printf "\nBUILD JAR\n"

jar cfm ProductSalePerCountry.jar src/Manifest.txt -C build .

printf "\nRUN MAP-REDUCE\n"

hadoop jar ProductSalePerCountry.jar sales_country.SalesCountryDriver /sales /sales_out

printf "\nRESULTS\n"

hdfs dfs -cat /sales_out/*

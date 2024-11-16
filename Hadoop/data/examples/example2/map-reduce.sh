#!/bin/bash
cd example2

printf "\nCOPY FILE TO HDFS\n"

hdfs dfs -rm -r -f /sales_out/
hdfs dfs -put SalesJan2009.csv /sales

printf "\nSET CLASSPATHS\n"

export CLASSPATH="$HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-client-core-$HADOOP_VERSION.jar:$HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-client-common-$HADOOP_VERSION.jar:$HADOOP_HOME/share/hadoop/common/hadoop-common-$HADOOP_VERSION.jar:~/example2/*:$HADOOP_HOME/lib/*"

printf "\nCOMPILE JAVA\n"

javac -d . src/*.java

printf "\nBUILD JAR\n"

jar cfm ProductSalePerCountry.jar src/Manifest.txt sales_country/*.class

printf "\nRUN MAP-REDUCE\n"

hadoop jar ProductSalePerCountry.jar sales_country.SalesCountryDriver /sales /sales_out

printf "\nRESULTS\n"

hdfs dfs -cat /sales_out/*
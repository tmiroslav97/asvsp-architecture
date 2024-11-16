#!/bin/bash
cd zadatak1

hdfs dfs -rm -r -f /mean_out_j

printf "\nSET CLASSPATHS\n"

export CLASSPATH="$HADOOP_PREFIX/share/hadoop/mapreduce/hadoop-mapreduce-client-core-$HADOOP_VERSION.jar:$HADOOP_PREFIX/share/hadoop/mapreduce/hadoop-mapreduce-client-common-$HADOOP_VERSION.jar:$HADOOP_PREFIX/share/hadoop/common/hadoop-common-$HADOOP_VERSION.jar:~/example1/*:$HADOOP_PREFIX/lib/*"

printf "\nCOMPILE JAVA\n"

javac -d . CalculateMean.java 

printf "\nBUILD JAR\n"

jar cfm CalculateMean.jar Manifest.txt *.class

printf "\nRUN MAP-REDUCE\n"

hadoop jar CalculateMean.jar CalculateMean /mean /mean_out_j

printf "\nRESULTS\n"

hdfs dfs -cat /mean_out_j/*
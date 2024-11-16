#!/bin/bash
cd example1

printf "\nCOPY FILE TO HDFS\n"

hdfs dfs -put sample.txt /units

printf "\nSET CLASSPATHS\n"

export CLASSPATH="$HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-client-core-$HADOOP_VERSION.jar:$HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-client-common-$HADOOP_VERSION.jar:$HADOOP_HOME/share/hadoop/common/hadoop-common-$HADOOP_VERSION.jar:~/example1/*:$HADOOP_HOME/lib/*"

printf "\nCOMPILE JAVA\n"

javac -d . ProcessUnits.java 

printf "\nBUILD JAR\n"

jar cfm ProcessUnits.jar Manifest.txt *.class

printf "\nRUN MAP-REDUCE\n"

hadoop jar ProcessUnits.jar ProcessUnits /units /units_out

printf "\nRESULTS\n"

hdfs dfs -cat /units_out/*
#!/bin/bash

echo "> Starting up cluster"
echo "> Creating docker network 'asvsp'"
docker network create asvsp

echo ">> Starting up HDFS"
docker compose -f Hadoop/docker-compose.yml up -d

echo ">> Starting up Hive"
docker compose -f Hive/docker-compose.yml up -d

echo ">> Starting up Apache Spark"
docker compose -f Apache-Spark/docker-compose.yml up -d

echo ">> Starting up Airflow"
docker compose -f Airflow/docker-compose.yml up -d

echo ">> Starting up Hue"
docker compose -f Hue/docker-compose.yml up -d

echo ">> Starting up Metabase"
docker compose -f Metabase/docker-compose.yml up -d

echo "> Services started sleeping for 25 seconds"

sleep 25

echo "> Configuring individual services"

echo ">> Setting up Airflow objects"
cmd='bash -c "/opt/airflow/config/setupObjects.sh"'
docker exec -it airflow-airflow-webserver-1 $cmd

echo ">> Starting up sshd servers"
cmd='bash -c "/usr/sbin/sshd"'
docker exec -it namenode $cmd
docker exec -it spark-master $cmd
docker exec -it hive-server $cmd
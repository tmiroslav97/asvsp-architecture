#!/bin/bash

echo "> Starting up cluster"
echo "> Creating docker network 'asvsp'"
docker network create asvsp

ssh_server_startup_cmd='bash -c "/usr/sbin/sshd"'

function exists_in_list() {
    LIST=$1
    DELIMITER=$2
    VALUE=$3
    LIST_WHITESPACES=`echo $LIST | tr "$DELIMITER" " "`
    for x in $LIST_WHITESPACES; do
        if [ "$x" = "$VALUE" ]; then
            return 0
        fi
    done
    return 1
}

list_of_services="hdfs hive spark airflow hue metabase kafka data_generator"
for service in "$@"
do
    if exists_in_list "$list_of_services" " " $service; then
        continue
    else
        echo "ERROR: Service $service not in the list of supported services! List of supported services: $list_of_services"
        echo "Exiting."
        exit 1
    fi
done

for service in "$@" 
do
    echo "Service - $i: $service";
    i=$((i + 1));
    case $service in
        'hdfs')
            echo ">> Starting up HDFS"
            docker compose -f Hadoop/docker-compose.yml up -d
            sleep 5
            docker exec -it namenode $ssh_server_startup_cmd
            ;;
        'hive')
            echo ">> Starting up Hive"
            docker compose -f Hive/docker-compose.yml up -d
            sleep 15
            docker exec -it hive-server $ssh_server_startup_cmd
            ;;
        'spark')
            echo ">> Starting up Apache Spark"
            docker compose -f Apache-Spark/docker-compose.yml up -d
            sleep 15
            docker exec -it spark-master $ssh_server_startup_cmd
            ;;
        'airflow')
            echo ">> Starting up Airflow"
            docker compose -f Airflow/docker-compose.yml up -d
            sleep 25
            echo ">> Setting up Airflow objects"
            cmd='bash -c "/opt/airflow/config/setupObjects.sh"'
            docker exec -it airflow-airflow-webserver-1 $cmd
            ;;
        'hue')
            echo ">> Starting up Hue"
            docker compose -f Hue/docker-compose.yml up -d
            ;;
        'metabase')
            echo ">> Starting up Metabase"
            docker compose -f Metabase/docker-compose.yml up -d
            ;;
        'kafka')
            # echo ">> Starting up Kafka"
            # docker compose -f Kafka/docker-compose.yml up -d
            # sleep 15
            cmd='bash -c "/opt/kafka/config/setupObjects.sh"'
            docker exec -it kafka-broker1-1 $cmd
            ;;
        'data_generator')
            echo ">> Starting up Data Generator"
            docker compose -f Data-Generator/docker-compose.yml up -d
            ;;
        *)
            echo ">> Service not recognized, skipping"
    esac
done
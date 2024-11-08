#!/bin/bash

echo "> Bringing down cluster services"

read -p "> Delete volumes? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo ">> Shutting down Metabase"
    docker compose -f Metabase/docker-compose.yml down -v

    echo ">> Shutting down Hue"
    docker compose -f Hue/docker-compose.yml down -v

    echo ">> Shutting down Airflow"
    docker compose -f Airflow/docker-compose.yml down -v

    echo ">> Shutting down Apache Spark"
    docker compose -f Apache-Spark/docker-compose.yml down -v

    echo ">> Shutting down Hive"
    docker compose -f Hive/docker-compose.yml down -v

    echo ">> Shutting down Hadoop"
    docker compose -f Hadoop/docker-compose.yml down -v

    echo ">> Shutting down Kafka"
    docker compose -f Kafka/docker-compose.yml down -v

    echo ">> Shutting down Data Generator"
    docker compose -f Data-Generator/docker-compose.yml down -v

else
    echo ">> Shutting down Metabase"
    docker compose -f Metabase/docker-compose.yml down -v
    
    echo ">> Shutting down Hue"
    docker compose -f Hue/docker-compose.yml down

    echo ">> Shutting down Airflow"
    docker compose -f Airflow/docker-compose.yml down

    echo ">> Shutting down Apache Spark"
    docker compose -f Apache-Spark/docker-compose.yml down

    echo ">> Shutting down Hive"
    docker compose -f Hive/docker-compose.yml down

    echo ">> Shutting down Hadoop"
    docker compose -f Hadoop/docker-compose.yml down

    echo ">> Shutting down Kafka"
    docker compose -f Kafka/docker-compose.yml down

    echo ">> Shutting down Data Generator"
    docker compose -f Data-Generator/docker-compose.yml down

fi

echo "> Deleting 'asvsp' network"
docker network rm asvsp
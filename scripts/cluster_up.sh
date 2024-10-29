#!/bin/bash

docker network create asvsp_network

# starting up hdfs
docker compose -f Hadoop/docker-compose.yml up -d

# starting up hdfs
#docker compose -f Hive/docker-compose.yml up -d

# starting up hue
docker compose -f Hue/docker-compose.yml up -d
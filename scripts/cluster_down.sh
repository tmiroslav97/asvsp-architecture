#!/bin/bash

#shutting down hue
docker compose -f Hue/docker-compose.yml down -v

# shutting down hdfs
#docker compose -f Hive/docker-compose.yml down -v

# shutting down hdfs
docker compose -f Hadoop/docker-compose.yml down -v

docker network rm asvsp_network
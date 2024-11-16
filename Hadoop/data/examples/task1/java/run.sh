#!/bin/bash
docker exec -it resourcemanager bash -c "rm -rf /zadatak1"
docker cp . resourcemanager:/zadatak1/
docker exec -it resourcemanager bash -c "chmod +x /zadatak1/map-reduce.sh && /zadatak1/map-reduce.sh"
# docker exec -it resourcemanager bash -c "hdfs dfs -rm -r -f /units*"
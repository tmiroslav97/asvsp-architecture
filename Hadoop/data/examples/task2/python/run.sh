#!/bin/bash
# docker exec -it nodemanager1 bash -c "apt update && apt install python -y"
# docker exec -it nodemanager2 bash -c "apt update && apt install python -y"

docker exec -it resourcemanager bash -c "rm -rf /zadatak2"
docker cp . resourcemanager:/zadatak2
docker exec -it resourcemanager bash -c "chmod +x /zadatak2/map-reduce.sh && /zadatak2/map-reduce.sh"
# docker exec -it resourcemanager bash -c "hdfs dfs -rm -r -f /mean*"
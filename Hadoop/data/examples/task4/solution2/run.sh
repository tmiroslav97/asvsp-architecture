#!/bin/bash
# docker exec -it nodemanager1 bash -c "apt update && apt install python -y"
# docker exec -it nodemanager2 bash -c "apt update && apt install python -y"

docker exec -it resourcemanager bash -c "rm -rf /zadatak4"
docker cp . resourcemanager:/zadatak4
docker exec -it resourcemanager bash -c "chmod +x /zadatak4/map-reduce.sh && /zadatak4/map-reduce.sh"
# docker exec -it resourcemanager bash -c "hdfs dfs -rm -r -f /friends*"
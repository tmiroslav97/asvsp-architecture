#!/bin/bash

# docker exec -it nodemanager1 bash -c "apt update && apt install python -y"
# docker exec -it nodemanager2 bash -c "apt update && apt install python -y"

docker cp . resourcemanager:/shpth
docker exec -it resourcemanager bash -c "chmod +x /shpth/map-reduce.sh && /shpth/map-reduce.sh"
docker exec -it resourcemanager bash -c "hdfs dfs -rm -r -f /shpth_*"
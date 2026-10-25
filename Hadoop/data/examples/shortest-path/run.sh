#!/bin/bash

docker cp . resourcemanager:/shpth
docker exec -it resourcemanager bash -c "chmod +x /shpth/map-reduce.sh && /shpth/map-reduce.sh"
docker exec -it resourcemanager bash -c "hdfs dfs -rm -r -f /shpth_*"
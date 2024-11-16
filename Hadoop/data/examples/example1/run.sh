#!/bin/bash
docker exec -it resourcemanager bash -c "hdfs dfs -rm -r -f /units*"
docker exec -it resourcemanager bash -c "rm -rf /example1"
docker cp . resourcemanager:/example1/
docker exec -it resourcemanager bash -c "chmod +x /example1/map-reduce.sh && /example1/map-reduce.sh"
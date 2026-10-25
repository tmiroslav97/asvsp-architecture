#!/bin/bash

docker exec -it resourcemanager bash -c "hdfs dfs -rm -r -f /book*"
docker exec -it resourcemanager bash -c "rm -rf /example3"
docker cp . resourcemanager:/example3
docker exec -it resourcemanager bash -c "chmod +x /example3/map-reduce.sh && /example3/map-reduce.sh"
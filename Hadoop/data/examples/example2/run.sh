#!/bin/bash
docker exec -it resourcemanager bash -c "hdfs dfs -rm -r -f /sales*"
docker exec -it resourcemanager bash -c "rm -rf /example2"
docker cp . resourcemanager:/example2/
docker exec -it resourcemanager bash -c "chmod +x /example2/map-reduce.sh && /example2/map-reduce.sh"
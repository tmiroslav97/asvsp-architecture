#!/bin/bash
set -euo pipefail

WORK_DIR=/opt/hadoop/shortest-path
docker exec -it --user root resourcemanager rm -rf "$WORK_DIR"
docker cp . "resourcemanager:$WORK_DIR/"
docker exec -it --user root resourcemanager chown -R hadoop:users "$WORK_DIR"
docker exec -it --user hadoop resourcemanager bash "$WORK_DIR/map-reduce.sh"
docker exec -it resourcemanager bash -c "hdfs dfs -rm -r -f /shpth_*"

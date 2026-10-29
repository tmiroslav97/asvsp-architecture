#!/bin/bash
set -euo pipefail

docker exec -it resourcemanager bash -c "hdfs dfs -rm -r -f /book*"
WORK_DIR=/opt/hadoop/example3
docker exec -it --user root resourcemanager rm -rf "$WORK_DIR"
docker cp . "resourcemanager:$WORK_DIR/"
docker exec -it --user root resourcemanager chown -R hadoop:users "$WORK_DIR"
docker exec -it --user hadoop resourcemanager bash "$WORK_DIR/map-reduce.sh"

#!/bin/bash
set -euo pipefail

TASK_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
WORK_DIR=/opt/hadoop/task3
docker exec --user root resourcemanager rm -rf "$WORK_DIR"
docker cp "$TASK_DIR/." "resourcemanager:$WORK_DIR"
docker exec --user root resourcemanager chown -R hadoop:users "$WORK_DIR"
docker exec --user hadoop resourcemanager bash "$WORK_DIR/python/map-reduce.sh"

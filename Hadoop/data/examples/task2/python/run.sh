#!/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
WORK_DIR=/opt/hadoop/task2
docker exec --user root resourcemanager rm -rf "$WORK_DIR"
docker cp "$SCRIPT_DIR/." "resourcemanager:$WORK_DIR"
docker exec --user root resourcemanager chown -R hadoop:users "$WORK_DIR"
docker exec --user hadoop resourcemanager bash "$WORK_DIR/map-reduce.sh"

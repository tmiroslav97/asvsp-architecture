#!/bin/bash
set -euo pipefail

TASK_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
docker exec resourcemanager rm -rf /task1
docker cp "$TASK_DIR/." resourcemanager:/task1
docker exec resourcemanager bash -lc 'chmod +x /task1/python/map-reduce.sh && /task1/python/map-reduce.sh'

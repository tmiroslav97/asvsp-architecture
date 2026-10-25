#!/bin/bash
set -euo pipefail

TASK_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
docker exec resourcemanager rm -rf /task3
docker cp "$TASK_DIR/." resourcemanager:/task3
docker exec resourcemanager bash -lc 'chmod +x /task3/python/map-reduce.sh && /task3/python/map-reduce.sh'

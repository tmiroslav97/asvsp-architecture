#!/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
docker exec resourcemanager rm -rf /task2
docker cp "$SCRIPT_DIR/." resourcemanager:/task2
docker exec resourcemanager bash -lc 'chmod +x /task2/map-reduce.sh && /task2/map-reduce.sh'

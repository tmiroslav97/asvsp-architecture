#!/bin/bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
docker exec resourcemanager rm -rf /task4
docker cp "$SCRIPT_DIR/." resourcemanager:/task4
docker exec resourcemanager bash -lc 'chmod +x /task4/map-reduce.sh && /task4/map-reduce.sh'

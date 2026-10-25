#!/usr/bin/env bash
set -euo pipefail

# Give every container its own server identity, then start SSH as root. Hive
# continues as its dedicated unprivileged account through the upstream entrypoint.
ssh-keygen -A
/usr/sbin/sshd
exec runuser -u hive -- /entrypoint.sh "$@"

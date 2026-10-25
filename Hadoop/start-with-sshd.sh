#!/usr/bin/env bash
set -euo pipefail

# Start SSH as root, then replace this process with Hadoop running as its
# dedicated unprivileged account. SSH remains available to other containers on
# the Compose network at port 22.
ssh-keygen -A
/usr/sbin/sshd
exec runuser -u hadoop -- /opt/starter.sh "$@"

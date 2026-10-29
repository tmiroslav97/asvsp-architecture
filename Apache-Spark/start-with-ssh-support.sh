#!/usr/bin/env bash
set -euo pipefail

# sshd is started on demand by scripts/cluster_up.sh, as in the previous image.
# Host keys must exist before that command is issued, but are generated per
# container rather than baked into the image.
ssh-keygen -A

# With `su -c`, the first argument after the account becomes the shell's $0.
# Supply a dummy value so every Spark command argument is retained in "$@".
exec su -s /bin/bash -c 'exec /opt/entrypoint.sh "$@"' spark spark "$@"

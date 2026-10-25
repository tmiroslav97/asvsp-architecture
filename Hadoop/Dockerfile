FROM apache/hadoop:3.5.0

# The official image runs as the unprivileged `hadoop` user. Pre-create the
# directories so Docker initializes each new named volume with usable ownership.
USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends openssh-server \
    && rm -rf /var/lib/apt/lists/* \
    && rm -f /etc/ssh/ssh_host_*_key /etc/ssh/ssh_host_*_key.pub \
    && mkdir -p /run/sshd /hadoop/dfs/name /hadoop/dfs/data /hadoop/yarn/timeline \
    && chown -R hadoop:hadoop /hadoop
RUN printf '%s\n' 'PermitRootLogin yes' 'PasswordAuthentication yes' \
      > /etc/ssh/sshd_config.d/00-asvsp.conf \
    && echo 'root:asvsp' | chpasswd
COPY --chown=hadoop:users config/ /opt/hadoop/etc/hadoop/
COPY start-with-sshd.sh /usr/local/bin/start-with-sshd.sh
RUN chmod 0755 /usr/local/bin/start-with-sshd.sh

EXPOSE 22
ENTRYPOINT ["/usr/local/bin/dumb-init", "--", "/usr/local/bin/start-with-sshd.sh"]

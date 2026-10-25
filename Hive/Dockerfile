FROM apache/hive:4.2.1

# Keep the SSH endpoint used by scripts/cluster_up.sh and add the JDBC driver
# required by the upstream image when PostgreSQL is used as the metastore.
USER root
RUN microdnf install -y openssh-server \
    && microdnf clean all \
    && mkdir -p /var/run/sshd \
    && rm -f /etc/ssh/ssh_host_*_key /etc/ssh/ssh_host_*_key.pub \
    && sed -ri 's/^[[:space:]]*#?[[:space:]]*PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && sed -ri 's/^[[:space:]]*#?[[:space:]]*PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config \
    && echo 'root:asvsp' | chpasswd \
    && curl --fail --location --retry 3 --output /opt/hive/lib/postgres.jar \
      https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.8/postgresql-42.7.8.jar

COPY start-with-sshd.sh /usr/local/bin/start-with-sshd.sh
RUN chmod 0755 /usr/local/bin/start-with-sshd.sh

EXPOSE 22
ENTRYPOINT ["/usr/local/bin/start-with-sshd.sh"]

FROM bde2020/hive:2.3.2-postgresql-metastore

RUN echo "deb http://archive.debian.org/debian stretch main" > /etc/apt/sources.list

RUN apt-get update && apt-get install -y openssh-server
RUN mkdir /var/run/sshd

RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
RUN echo '# Hadoop config\nexport HADOOP_HOME=/opt/hadoop-2.7.4' >> /opt/hive/bin/hive-config.sh \
    && echo 'export HADOOP_PREFIX=/opt/hadoop-2.7.4' >> /opt/hive/bin/hive-config.sh \
    && echo 'export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/' >> /opt/hive/bin/hive-config.sh
RUN echo "root:asvsp" | chpasswd

EXPOSE 22
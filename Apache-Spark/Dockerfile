FROM apache/spark:4.2.0-java17

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends openssh-server python3 python3-pip curl netcat-openbsd \
    && python3 -m pip install --no-cache-dir 'numpy>=1.23,<3' \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /run/sshd /opt/hadoop-conf \
    && ln -s /opt/spark /spark \
    && sed -ri 's/^[[:space:]]*#?[[:space:]]*PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && sed -ri 's/^[[:space:]]*#?[[:space:]]*PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config \
    && echo 'root:asvsp' | chpasswd

RUN mkdir -p /tmp/ivy \
    && /opt/spark/bin/spark-submit \
      --conf spark.jars.ivy=/tmp/ivy \
      --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.2.0 \
      --class org.apache.spark.examples.SparkPi \
      /opt/spark/examples/jars/spark-examples_2.13-4.2.0.jar 1 \
    && cp /tmp/ivy/jars/*.jar /opt/spark/jars/ \
    && rm -rf /tmp/ivy

COPY config/core-site.xml /opt/hadoop-conf/core-site.xml
COPY config/spark-defaults.conf /opt/spark/conf/spark-defaults.conf
COPY start-with-ssh-support.sh /usr/local/bin/start-with-ssh-support.sh
RUN chmod 0755 /usr/local/bin/start-with-ssh-support.sh

ENV HADOOP_CONF_DIR=/opt/hadoop-conf \
    PYSPARK_PYTHON=python3

EXPOSE 22
ENTRYPOINT ["/usr/local/bin/start-with-ssh-support.sh"]

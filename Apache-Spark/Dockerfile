FROM bde2020/spark-master:3.0.1-hadoop3.2

RUN apk update && apk add openssh-server
RUN mkdir /var/run/sshd
RUN ssh-keygen -A

RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
RUN echo 'export JAVA_HOME=/usr/lib/jvm/java-1.8-openjdk/' >> /spark/bin/load-spark-env.sh
RUN echo "root:asvsp" | chpasswd

EXPOSE 22
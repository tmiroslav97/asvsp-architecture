FROM apache/hive:4.2.1

# Add the JDBC driver required by the upstream image when PostgreSQL is used as
# the metastore.
USER root
RUN curl --fail --location --retry 3 --output /opt/hive/lib/postgres.jar \
      https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.8/postgresql-42.7.8.jar

USER hive

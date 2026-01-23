FROM maven AS maven_build

COPY pom.xml /usr/pom.xml
RUN mvn -f /usr/pom.xml clean package

COPY . /usr/
RUN mvn -f /usr/pom.xml clean package -o

FROM eclipse-temurin:21-jre
COPY --from=maven_build /usr/target /usr
CMD ["java", "-cp", "/usr/kafka-streams-demo-1.0-SNAPSHOT.jar:/usr/target/libraries/*", "com.example.kafka_streams_examples.BranchByProtocol"]

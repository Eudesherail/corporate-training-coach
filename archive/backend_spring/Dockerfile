# FROM maven:3.6.1-jdk-8-slim AS build
# RUN mkdir -p /workspace
# WORKDIR /workspace
# COPY pom.xml /workspace
# COPY src /workspace/src
# RUN mvn -f pom.xml clean package

# FROM openjdk:8-alpine
# COPY --from=build /workspace/target/*.jar app.jar
# EXPOSE 8080
# ENTRYPOINT ["java","-jar","app.jar"]

# Start with a base image containing Java runtime
FROM openjdk:19-slim

# Add Maintainer Info
LABEL maintainer="email@example.com"

# Add a volume pointing to /tmp
VOLUME /tmp

# Make port available to the world outside this container
EXPOSE 8080

RUN apt-get update && \
    apt-get install -y maven && \
    rm -rf /var/lib/apt/lists/*
# The application's source code
WORKDIR /usr/src/app
COPY . .

# Build with maven wrapper
RUN mvn clean install -DskipTests

# Run the jar file 
ENTRYPOINT ["java","-jar","target/studybuddy-0.0.1-SNAPSHOT.jar"]


# --- Etapa 1: Construcción (Build) ---
FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /app

# Copiar archivos del proyecto
COPY pom.xml .
COPY src ./src

# Compilar y empaquetar
RUN mvn clean package -DskipTests

# --- Etapa 2: Ejecución (Run) ---
FROM tomcat:10-jdk17-temurin

# Limpiar aplicaciones por defecto
RUN rm -rf /usr/local/tomcat/webapps/*

# Copiar el WAR generado en la etapa anterior
COPY --from=build /app/target/Practica6_SW.war /usr/local/tomcat/webapps/ROOT.war

EXPOSE 8080
CMD ["catalina.sh", "run"]
# --- Etapa 1: Construcción (Build) ---
# Usamos una imagen con Maven para compilar el proyecto
FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /app

# Copiamos el archivo de configuración y el código fuente
COPY pom.xml .
COPY src ./src

# Ejecutamos Maven para crear el archivo .war
RUN mvn clean package -DskipTests

# --- Etapa 2: Ejecución (Run) ---
# Usamos la imagen de Tomcat para servir la app
FROM tomcat:10-jdk17-temurin

# Limpiamos las apps por defecto de Tomcat
RUN rm -rf /usr/local/tomcat/webapps/*

# Copiamos el .war GENERADO en la Etapa 1 a la carpeta de Tomcat
# Nota cómo usamos "--from=build" para traer el archivo de la etapa anterior
COPY --from=build /app/target/Practica6_SW.war /usr/local/tomcat/webapps/ROOT.war

EXPOSE 8080
CMD ["catalina.sh", "run"]
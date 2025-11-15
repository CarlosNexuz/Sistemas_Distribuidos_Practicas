# ----------------------------
# Dockerfile para Practica6_SW
# ----------------------------

FROM tomcat:10-jdk17-temurin

# Limpiar cualquier aplicación previa
RUN rm -rf /usr/local/tomcat/webapps/*

# Copiar WAR y renombrar a ROOT.war
COPY target/Practica6_SW.war /usr/local/tomcat/webapps/ROOT.war

EXPOSE 8080

CMD ["catalina.sh", "run"]

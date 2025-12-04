# Etapa 1: construir la aplicación
FROM node:18-alpine AS build

#p1
# Crear el directorio de la aplicación dentro del contenedor
WORKDIR /app

# Copiar los archivos de configuración y dependencias
COPY package*.json ./

# Instalar las dependencias
RUN npm install

# Copiar el resto del proyecto
COPY . .

# Construir la aplicación para producción
RUN npm run build

# Etapa 2: servir la aplicación con un servidor web liviano (Nginx)
FROM nginx:stable-alpine

# Copiar los archivos generados por React al servidor Nginx
COPY --from=build /app/build /usr/share/nginx/html

# Exponer el puerto 80 para que la app sea accesible
EXPOSE 80

# Comando para ejecutar Nginx en modo "foreground"
CMD ["nginx", "-g", "daemon off;"]

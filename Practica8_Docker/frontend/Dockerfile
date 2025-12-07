# Usamos la imagen oficial ligera de Nginx
FROM nginx:1.25-alpine

# 1. Copiamos tu HTML al directorio público de Nginx
COPY index.html /usr/share/nginx/html/index.html

# 2. Copiamos la plantilla de configuración
# La imagen nginx:alpine buscará archivos *.template en esta ruta
# y usará 'envsubst' para reemplazar las variables automáticamente.
COPY nginx.conf.template /etc/nginx/templates/default.conf.template

# Exponemos el puerto 8080 (estándar para Cloud Run)
EXPOSE 8080

# El comando por defecto de la imagen ya se encarga de todo
CMD ["nginx", "-g", "daemon off;"]
# Usa una imagen base oficial de Python
FROM python:3.9-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requisitos e instala las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Expone el puerto que usará Flask (8080 es el estándar de Cloud Run)
EXPOSE 8080

# Comando para ejecutar la aplicación usando el script python modificado
CMD ["python", "app.py"]
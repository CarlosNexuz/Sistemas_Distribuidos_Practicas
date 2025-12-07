# Usa una imagen base oficial de Python
FROM python:3.9-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requisitos e instala las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Expone el puerto que usará Flask
EXPOSE 5000

# Comando para ejecutar la aplicación cuando el contenedor arranque
# Usa 0.0.0.0 para que el servidor Flask sea accesible desde fuera del contenedor
# CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
CMD ["python", "app.py"]
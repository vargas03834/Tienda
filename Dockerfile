# Usa una imagen oficial de Python
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /ec

# Copia los archivos del proyecto al contenedor
COPY . /ec

# Instala dependencias del sistema necesarias para Python y PostgreSQL
RUN apt-get update && apt-get install -y gcc libpq-dev

# Instala las dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expone el puerto donde corre Django
EXPOSE 8000

# Comando para ejecutar el servidor de desarrollo de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

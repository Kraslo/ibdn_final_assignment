# AUTHORED BY IGNACIO ESCRIBANO AND DARÍO COBO
# GNU GENERAL PUBLIC LICENSE (GPL) 3.0
# RUN THIS DOCKERFILE FROM THE BASE PROJECT PATH, OTHERWISE IT WON'T WORK

# Utilizamos una imagen base de Python 3.9
FROM python:3.6-slim

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos el archivo de requisitos y los instalamos
COPY practica_creativa/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

USER root
RUN apt-get update && apt-get -y install procps
USER 1001
# Copiamos el resto de la aplicación al contenedor
COPY practica_creativa .

# train model
# WORKDIR /app # REDUNDANT
# RUN python3 resources/train_spark_mllib_model.py .

# Exponemos el puerto en el que Flask correrá
EXPOSE 5001 
# pongo 5001 porque en predict_flask.py está así especificado.

# Definimos el comando de inicio
ENTRYPOINT ["python3", "/app/resources/web/predict_flask.py"]

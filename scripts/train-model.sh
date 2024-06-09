#!/bin/bash

# Verificar si se proporcionan los argumentos necesarios
if [ $# -ne 3 ]; then
    echo "Uso: $0 <nombre_del_contenedor> <ruta_del_script>"
    exit 1
fi

# Extraer los argumentos
CONTAINER_NAME=$1
SCRIPT_PATH=$2
ARG_PATH=$3

# Ejecutar el script dentro del contenedor Docker con privilegios de superusuario
docker exec -u 0 "$CONTAINER_NAME" python3 "$SCRIPT_PATH" "$ARG_PATH"

# Comprobar el código de salida del comando anterior
if [ $? -ne 0 ]; then
    echo "Error al ejecutar el script dentro del contenedor."
    exit 1
fi

echo "Script ejecutado correctamente dentro del contenedor."

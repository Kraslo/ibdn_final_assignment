FROM mongo:6.0

WORKDIR /pcreativa

RUN mkdir -p /data/db && chown -R mongodb:mongodb /data/db

RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz | tar -C /usr/local/bin -xzv

COPY practica_creativa .
COPY mongodocker/importscript.js /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/importscript.js

USER root

#RUN ls 
RUN /pcreativa/resources/download_data.sh


#USER 1001
# Copy downloaded data to data_volume
# RUN cp -r /pcreativa/data /data_volume # just gonna mount the data volume, so this command is no longer needed

# Iniciar MongoDB en segundo plano y usar dockerize para esperar a que esté disponible
#RUN mongod --fork --logpath /var/log/mongodb.log --dbpath /data/db && \
#    dockerize -wait tcp://localhost:27017 -timeout 30s && \
#    ./resources/import_distances.sh
EXPOSE 27017
#CMD ["sh", "-c", "cp -r /pcreativa/data/* /data_ibdn/"]
#CMD ["sh", "-c", "/pcreativa/resources/import_distances.sh"]


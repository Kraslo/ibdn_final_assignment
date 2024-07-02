FROM apache/spark:3.3.3

USER root
RUN apt-get update
RUN apt-get install -y unzip curl zip
RUN curl -L -o sbt.zip https://github.com/sbt/sbt/releases/download/v1.5.5/sbt-1.5.5.zip && \
    unzip sbt.zip -d /usr/local && \
    rm sbt.zip && \
    ln -s /usr/local/sbt/bin/sbt /usr/local/bin/sbt

WORKDIR /app

COPY practica_creativa .
COPY sparkdocker/start-spark.sh /usr/local/bin/start-spark.sh

RUN chmod +x /usr/local/bin/start-spark.sh

ENTRYPOINT ["/usr/local/bin/start-spark.sh"]

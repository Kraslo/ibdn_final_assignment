FROM bitnami/kafka:3.4

WORKDIR /opt/bitnami/kafka

COPY kafkadocker/start-kafka.sh /opt/bitnami/kafka/start-kafka.sh

# Give execute permissions to the script
USER root
RUN chmod +x /opt/bitnami/kafka/start-kafka.sh
USER 1001

ENTRYPOINT ["/opt/bitnami/kafka/start-kafka.sh"]


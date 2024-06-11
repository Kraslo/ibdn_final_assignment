#!/bin/bash

/opt/bitnami/kafka/bin/zookeeper-server-start.sh /opt/bitnami/kafka/config/zookeeper.properties &


sleep 15

cp /opt/bitnami/kafka/config/server.properties.original /opt/bitnami/kafka/config/server.properties

# Apply env variables set in docker-compose or pod configuration
if [[ ! -z "${KAFKA_CFG_ADVERTISED_LISTENERS}" ]]; then
  echo "advertised.listeners=${KAFKA_CFG_ADVERTISED_LISTENERS}" >> /opt/bitnami/kafka/config/server.properties
fi

if [[ ! -z "${KAFKA_CFG_LISTENERS}" ]]; then
  echo "listeners=${KAFKA_CFG_LISTENERS}" >> /opt/bitnami/kafka/config/server.properties
fi

if [[ ! -z "${KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP}" ]]; then
  echo "listener.security.protocol.map=${KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP}" >> /opt/bitnami/kafka/config/server.properties
fi

if [[ ! -z "${KAFKA_CFG_NODE_ID}" ]]; then
  echo "node.id=${KAFKA_CFG_NODE_ID}" >> /opt/bitnami/kafka/config/server.properties
fi

generate_uuid() {
  cat /proc/sys/kernel/random/uuid
}

echo "controller.quorum.registration.timeout.ms=30000" >> /opt/bitnami/kafka/config/server.properties

UUID=$(generate_uuid)
KAFKA_CLUSTER_ID="$(/opt/bitnami/kafka/bin/kafka-storage.sh random-uuid)"
/opt/bitnami/kafka/bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c /opt/bitnami/kafka/config/server.properties
/opt/bitnami/kafka/bin/kafka-server-start.sh /opt/bitnami/kafka/config/server.properties &

# Wait for server initialization
sleep 15

# Create the topics
/opt/bitnami/kafka/bin/kafka-topics.sh --create --bootstrap-server kafkaibdn:9092 --replication-factor 1 --partitions 1 --topic flight_delay_classification_request
/opt/bitnami/kafka/bin/kafka-topics.sh --create --bootstrap-server kafkaibdn:9092 --replication-factor 1 --partitions 1 --topic flight_predictions


# DO NOT STOP CONTAINER
tail -f /dev/null

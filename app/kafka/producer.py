from kafka import KafkaProducer
import json


producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)


def publish_transaction(transaction):

    producer.send(
        "transactions",
        transaction.model_dump(mode="json")
    )

    producer.flush()

    print(f"Published transaction {transaction.transaction_id}")
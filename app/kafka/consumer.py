from kafka import KafkaConsumer
import json

from app.schemas.transaction import Transaction
from app.database.repository import save_transaction


consumer = KafkaConsumer(
    "transactions",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    group_id="payflow-consumer",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)


print("Waiting for transactions...\n")


for message in consumer:

    try:
        transaction = Transaction(**message.value)

        save_transaction(transaction)

        print(
            f"Saved transaction {transaction.transaction_id} to PostgreSQL"
        )

    except Exception as e:
        print(f"Error processing message: {e}")
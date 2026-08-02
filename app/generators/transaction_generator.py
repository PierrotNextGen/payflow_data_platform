import time

from app.services.transaction_service import generate_transaction


def start_generator():
    while True:
        transaction = generate_transaction()
        print(transaction.model_dump_json(indent=2))
        print("-" * 80)
        time.sleep(1)


if __name__ == "__main__":
    start_generator()
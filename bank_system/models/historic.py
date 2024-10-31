from datetime import datetime


class Historic:
    def __init__(self) -> None:
        self._transactions = []

    @property
    def transactions(self) -> list:
        return self._transactions

    def add_transaction(self, transaction):
        new_transaction = {
            "type_transaction": transaction.__class__.__name__,
            "value": transaction.value,
            "created_at": datetime.now().strftime("%d-%m-%Y | %H:%M:%S"),
        }
        self._transactions.append(new_transaction)

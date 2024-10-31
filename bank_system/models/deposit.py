from models.transaction import Transaction


class Deposit(Transaction):
    def __init__(self, value) -> None:
        super().__init__()
        self._value = float(value)

    @property
    def value(self) -> float:
        return self._value

    def register(self, account):
        value = self._value
        account.deposit(value)

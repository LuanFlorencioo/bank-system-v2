from models.historic import Historic


class Account:
    def __init__(self, number, client, bank) -> None:
        self._balance = float(0)
        self._number = number
        self._agency = "0001"
        self._client = client
        self._bank = bank
        self._historic = Historic()

    @property
    def balance(self) -> float:
        return self._balance

    @property
    def bank(self) -> str:
        return self._bank

    @property
    def historic(self):
        return self._historic

    @classmethod
    def new_account(cls, number, client, bank):
        return cls(number, client, bank)

    def withdrawal(self, value) -> bool:
        if value <= self._balance and value > 0:
            self._balance -= value
            return True
        else:
            return False

    def deposit(self, value) -> bool:
        if value > 0:
            self._balance += value
            return True
        else:
            return False

    def __str__(self) -> str:
        return f"Titular: {self._client.name.upper()}\n\tBanco: {self._bank}\n\tN° c/c: {self._number}\n\tAgência: {self._agency}"

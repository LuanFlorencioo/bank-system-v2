from models.account import Account


class CheckingAccount(Account):
    def __init__(
        self, number, client, bank, withdrawal_count_limit=3, withdrawal_value_limit=500
    ) -> None:
        super().__init__(number, client, bank)
        self._withdrawal_count_limit = withdrawal_count_limit
        self._withdrawal_value_limit = float(withdrawal_value_limit)

    @property
    def withdrawal_count_limit(self) -> int:
        return self._withdrawal_count_limit

    @property
    def withdrawal_value_limit(self) -> float:
        return self._withdrawal_value_limit

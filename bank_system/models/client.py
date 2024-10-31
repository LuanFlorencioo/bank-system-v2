class Client:
    def __init__(self, address) -> None:
        self._address = address
        self._accounts = []

    def create_transaction(self, account, transaction) -> None:
        transaction.register(account)
        account.historic.add_transaction(transaction)

    def add_account(self, account) -> None:
        self._accounts.append(account)

    @property
    def accounts_count(self) -> int:
        return len(self._accounts)

    @property
    def accounts(self) -> list:
        return self._accounts

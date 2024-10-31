from models.user import User


class BankSystemDatabase:
    def __init__(self) -> None:
        self._clients = []  # keep all clients created
        self._accounts = []  # keep all accounts created
        self._clients.append(
            User(
                name="Luan Florencio",
                address="242, Roxo - Mrapic - Nova Iguaçu/RK",
                birth_date="13-05-2002",
                cpf="186.114.537-35",
                gender="Masculino",
            )
        )

    @property
    def clients(self) -> list:
        return self._clients

    @property
    def accounts(self) -> list:
        return self._accounts

    def add_client(self, client) -> None:
        self._clients.append(client)

    def add_account(self, account) -> None:
        self._accounts.append(account)

    def exists_client(self, cpf) -> bool:
        clients = self._clients
        exists = len([client for client in clients if client._cpf == cpf]) == 1
        return exists

    def find_client(self, cpf):
        client = [c for c in self._clients if c.cpf == cpf][0]
        return client

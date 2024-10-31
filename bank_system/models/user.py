from models.client import Client
from datetime import datetime


class User(Client):
    def __init__(self, name, cpf, gender, address, birth_date) -> None:
        super().__init__(address)
        self._name = name
        self._cpf = cpf
        self._gender = gender
        self._birth_date = birth_date
        self._created_at = datetime.now()

    @property
    def name(self):
        return self._name

    @property
    def cpf(self):
        return self._cpf

    def __str__(self) -> str:
        return f"nome: {self._name.upper()}\n\tCPF: {self._cpf}\n\tcontas associadas: {self.accounts_count}"

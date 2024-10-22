from datetime import datetime

class BankSystemInit():
    def __init__(self) -> None:
        self.balance = float(0)
        self.transactions = []
        self.users = []
        self.accounts = []
        self.withdrawal_count = 0
        self.WITHDRAWAL_LIMIT = 3
        self.WITHDRAWAL_VALUE_LIMIT = float(500)

    def update_balance(self, value) -> None:
        self.balance = value

    def create_transaction(self, *, transaction_type, value) -> None:
        transaction = {
            "type": "deposit" if transaction_type == "deposit" else "withdrawal",
            "value": float(value),
            "created_at": datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        }
        self.transactions.append(transaction)
    
    def is_allow_withdrawal(self) -> bool:
        is_limit = self.withdrawal_count < self.WITHDRAWAL_LIMIT

        return is_limit
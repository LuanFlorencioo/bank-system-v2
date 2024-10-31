import inquirer
from database import BankSystemDatabase
from utils import mouths, years, genders, confirm_choice, banks
from models import User, CheckingAccount, Deposit, Withdrawal
from datetime import datetime


def main():
    db = BankSystemDatabase()
    print("Olá! Seja bem-vindo(a) ao sistema bancário em python")

    while True:
        main_choice = (
            inquirer.list_input(
                message="Escolha alguma das operações a seguir",
                choices=[
                    "Depositar",
                    "Sacar",
                    "Extrato",
                    "Novo Usuário",
                    "Criar Conta Corrente",
                    "Ver Saldo",
                    "Listar Usuários",
                    "Listar Contas Corrente",
                    "Fechar Sistema",
                ],
            ),
        )[0]

        if main_choice == "Fechar Sistema":
            confirm = inquirer.list_input(
                message="Deseja realmente sair do sistema?",
                choices=["Sim", "Não"],
            )

            if confirm == "Sim":
                print("Muito bem, estamos fechando o sistema! Até logo")
                break

        elif main_choice == "Listar Usuários":
            clients = db.clients

            if len(clients) == 0:
                print("Nenhum usuário cadastrado ainda")

            else:
                print("----------------------------------------")
                for client in clients:
                    print(str(client))
                print(f"\nTodos os usuários cadastrado ({len(clients)})")
                print("----------------------------------------")
                input("Pressione [Enter] para continuar...")

        elif main_choice == "Listar Contas Corrente":
            accounts = db.accounts

            if len(accounts) == 0:
                print("Nenhuma foi criada ainda!")

            else:
                print("----------------------------------------")
                for account in accounts:
                    print(str(account))
                print(f"\nTodas as contas criadas ({len(accounts)})")
                print("----------------------------------------")
                input("Pressione [Enter] para continuar...")

        elif main_choice == "Novo Usuário":
            if confirm_choice("cadastrar novo usuário"):
                print("OK! Seguiremos então com o cadastro de um novo usuário.")
                print("Por favor, informe os dados abaixo:")

                client_cpf = inquirer.text(message="CPF")
                exists_cpf = db.exists_client(client_cpf)

                if exists_cpf:
                    print(
                        "Usuário já está cadastrado com esse CPF, com isso, não pode ser possível ter dois usuários com o mesmo CPF"
                    )
                    input("Pressione [Enter] para retornar")
                else:
                    client_data = inquirer.prompt(
                        [
                            inquirer.Text(name="first_name", message="Primeiro nome"),
                            inquirer.Text(name="last_name", message="Sobrenome"),
                            inquirer.List(
                                name="gender",
                                message="Gênero",
                                choices=genders,
                            ),
                        ]
                    )
                    print(
                        "Insira abaixo os dados referente a sua data de nascimento abaixo"
                    )
                    client_birthdate = inquirer.prompt(
                        [
                            inquirer.Text(name="day", message="Dia"),
                            inquirer.List(
                                name="mouth",
                                message="Mês de nascimento",
                                choices=mouths,
                            ),
                            inquirer.List(
                                name="year",
                                message="Ano de nascimento",
                                choices=years,
                            ),
                        ]
                    )
                    print(
                        "Insira abaixo os dados referente a sua localidade e residência"
                    )
                    client_address = inquirer.prompt(
                        [
                            inquirer.Text(name="city", message="Cidade"),
                            inquirer.Text(name="neighborhood", message="Bairro"),
                            inquirer.Text(
                                name="state",
                                message="Sigla do estado (UF)",
                            ),
                            inquirer.Text(name="street", message="Rua"),
                            inquirer.Text(
                                name="street_number", message="N° da residência"
                            ),
                        ]
                    )
                    client = User(
                        name=f"{client_data["first_name"]} {client_data["last_name"]}",
                        cpf=client_cpf,
                        gender=client_data["gender"],
                        address=f"{client_address["street"]}, {client_address["street_number"]} - {client_address["neighborhood"]} - {client_address["city"]}/{client_address["state"]}",
                        birth_date=datetime(
                            int(client_birthdate["year"]),
                            int(client_birthdate["mouth"]),
                            int(client_birthdate["day"]),
                        ).date(),
                    )
                    db.add_client(client)
                    print("Usuário criado com sucesso!")
                    input("Pressione [Enter] para prosseguir...")

        elif main_choice == "Criar Conta Corrente":
            if confirm_choice("criar uma conta corrente"):
                print(
                    "OK! Então seguiremos com o procedimento de associar uma nova conta"
                )
                print("Por favor, informe os dados abaixo:")

                client_cpf = inquirer.text(message="CPF")
                exists_cpf = db.exists_client(client_cpf)

                if not exists_cpf:
                    print(
                        "Não foi encontrado nenhum usuário com esse CPF cadastrado! Tente novamente mais tarde"
                    )
                else:
                    account_number = str(len(db.accounts) + 1)
                    client = db.find_client(client_cpf)
                    bank = inquirer.list_input(
                        message="Escolha o banco na qual gostaria de criar uma nova conta corrente",
                        choices=banks,
                    )
                    is_unique_bank = (
                        len(
                            [
                                account
                                for account in client.accounts
                                if account.bank == bank
                            ]
                        )
                        == 0
                    )

                    if is_unique_bank:
                        account = CheckingAccount(account_number, client, bank)
                        client.add_account(account)
                        db.add_account(account)
                        print("Conta corrente criada com sucesso")
                    else:
                        print(
                            f"Já existe uma conta corrente {bank} cadastrada nesse CPF"
                        )

                input("Pressione [Enter] para continuar...")

        elif main_choice == "Depositar":
            if confirm_choice("depósito bancário"):
                print(
                    "OK! Então seguiremos com o procedimento de depositar um valor bancário"
                )
                print("Por favor, informe os dados abaixo:")

                client_cpf = inquirer.text(message="CPF")
                exists_cpf = db.exists_client(client_cpf)

                if not exists_cpf:
                    print(
                        "Não foi encontrado nenhum usuário com esse CPF cadastrado! Tente novamente mais tarde"
                    )
                else:
                    client = db.find_client(client_cpf)

                    if client.accounts_count > 0:
                        client_accounts = client.accounts
                        client_banks = [account.bank for account in client_accounts]
                        bank = inquirer.list_input(
                            message="Escolha para qual banco você quer realizar o depósito",
                            choices=client_banks,
                        )
                        print("Insira o valor de depósito:")
                        value = input("\t↳ R$ ")
                        account = [
                            account
                            for account in client_accounts
                            if account.bank == bank
                        ][0]
                        transaction = Deposit(value)
                        client.create_transaction(account, transaction)
                        print("Depósito realizado com sucesso!")
                    else:
                        print(
                            "Não existe nenhuma conta corrente cadastrada nesse CPF para realizar um depósito"
                        )
                input("Pressione [Enter] para retornar")

        elif main_choice == "Ver Saldo":
            print("Informe o CPF referente ao titular de conta corrente:")
            client_cpf = inquirer.text(message="CPF")
            exists_cpf = db.exists_client(client_cpf)

            if not exists_cpf:
                print("Não foi encontrado nenhum usuário com esse CPF cadastrado!")
            else:
                client = db.find_client(client_cpf)

                if client.accounts_count > 0:
                    accounts = client.accounts
                    print("------------------- Saldo -------------------")
                    for account in accounts:
                        print(f"{account.bank}: R$ {account.balance:.2f}")
                    print("---------------------------------------------")
                else:
                    print("Não existe nenhuma conta corrente associada a este CPF")
            input("Pressione [Enter] para retornar")

        elif main_choice == "Extrato":
            print("Informe o CPF referente ao titular de conta corrente:")
            client_cpf = inquirer.text(message="CPF")
            exists_cpf = db.exists_client(client_cpf)

            if not exists_cpf:
                print("Não foi encontrado nenhum usuário com esse CPF cadastrado!")
            else:
                client = db.find_client(client_cpf)

                if client.accounts_count > 0:
                    client_accounts = client.accounts
                    client_banks = [account.bank for account in client_accounts]
                    bank = inquirer.list_input(
                        message="Escolha para qual banco você gostaria de ver o extrato",
                        choices=client_banks,
                    )
                    account = [
                        account for account in client_accounts if account.bank == bank
                    ][0]
                    transactions = account.historic.transactions

                    if not transactions:
                        print("Não foram realizadas transações")
                    else:
                        print("------------------- Extrato -------------------")
                        for transaction in transactions:
                            type_transaction = (
                                "Depósito"
                                if transaction["type_transaction"] == "Deposit"
                                else "Saque"
                            )
                            print(
                                f"{transaction["created_at"]} - {type_transaction} - R$ {transaction["value"]}"
                            )
                        print("-----------------------------------------------")

                else:
                    print(
                        "Não existe nenhuma conta corrente cadastrada nesse CPF para realizar um depósito"
                    )
            input("Pressione [Enter] para retornar")

        elif main_choice == "Sacar":
            if confirm_choice("saque bancário"):
                print("OK! Então seguiremos com o procedimento de saque bancário")
                print("Por favor, informe os dados abaixo:")

                client_cpf = inquirer.text(message="CPF")
                exists_cpf = db.exists_client(client_cpf)

                if not exists_cpf:
                    print(
                        "Não foi encontrado nenhum usuário com esse CPF cadastrado! Tente novamente mais tarde"
                    )
                else:
                    client = db.find_client(client_cpf)
                    client_accounts = client.accounts

                    if not client_accounts:
                        print(
                            "Não existe nenhuma conta corrente cadastrada nesse CPF para realizar um depósito"
                        )
                    else:
                        client_banks = [account.bank for account in client_accounts]
                        bank = inquirer.list_input(
                            message="Escolha para qual banco você quer realizar o saque",
                            choices=client_banks,
                        )
                        account = [
                            account
                            for account in client_accounts
                            if account.bank == bank
                        ][0]

                        if account.balance == 0:
                            print(f"Não há saldo suficiente!")
                        else:
                            transactions = account.historic.transactions
                            withdrawal_today = []
                            allow_withdrawal = True

                            for transaction in transactions:
                                transaction_date = transaction["created_at"]
                                transaction_date_parsed = datetime.strptime(
                                    transaction_date, "%d-%m-%Y | %H:%M:%S"
                                )
                                if (
                                    transaction_date_parsed.date()
                                    == datetime.today().date()
                                    and transaction["type_transaction"] == "Withdrawal"
                                ):
                                    withdrawal_today.append(transaction)
                                if (
                                    len(withdrawal_today)
                                    >= account.withdrawal_count_limit
                                ):
                                    allow_withdrawal = False
                                    break

                            if not allow_withdrawal:
                                print(
                                    f"Você atingiu o limite diário de saque que no total foram {account.withdrawal_count_limit}"
                                )
                            else:
                                print("Insira o valor de saque:")
                                value = float(input("\t↳ R$ "))

                                if value > account.withdrawal_value_limit:
                                    print(
                                        f"Não foi possível realizar o saque devido ao valor exceder o limite de R$ {account.withdrawal_value_limit:.2f}"
                                    )
                                elif value > account.balance:
                                    print("Saldo insuficiente")
                                else:
                                    transaction = Withdrawal(value)
                                    client.create_transaction(account, transaction)
                                    print("Saque realizado com sucesso!")

                input("Pressione [Enter] para retornar")


main()

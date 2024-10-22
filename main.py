from bank_system_init import BankSystemInit

bank = BankSystemInit()

def deposit(value, /) -> str:
    bank.update_balance(bank.balance + value)
    bank.create_transaction(transaction_type="deposit", value=value)
    message = f"O valor de R$ {value:.2f} foi depositado da sua conta com sucesso!"
    return message

def withdrawal(*, value) -> str:
    bank.update_balance(bank.balance - value)
    bank.create_transaction(transaction_type="withdrawal", value=value)
    bank.withdrawal_count += 1
    message = f"O valor de R$ {value:.2f} foi sacado da sua conta com sucesso!"
    return message

def extract(current_balance, /, *, transactions) -> None:
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    for transaction in transactions:
        transaction_type = "🟢 DEPÓSITO" if transaction["type"] == "deposit" else "🔴 SAQUE"
        print(f"| {transaction["created_at"]} | {transaction_type} | R$ {transaction["value"]:.2f}")

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
    print(f"Seu saldo atual é de: R$ {current_balance:.2f}")

def find_user(cpf):
    user = [u for u in bank.users if u["cpf"] == cpf]
    return user[0] if len(user) > 0 else None

def create_user(data):
    try:
        if not find_user(data["cpf"]):
            user_data = {
                "name": data["name"].upper(),
                "birthdate": data["birthdate"],
                "cpf": data["cpf"],
                "address": data["address"],
            }
            bank.users.append(user_data)
            print("Usuário criado com sucesso!")
        else:
            print("Já existe cadastrado um usuário com esse CPF!")
        
    except:
        print("Não foi possível criar um novo usuário")

def create_account(cpf):
    user = find_user(cpf)

    if user:
        new_account_number = len(bank.accounts) + 1
        bank.accounts.append({
            "agency": "0001",
            "account_number": new_account_number,
            "user": user["name"]
        })
        print("Conta criada com sucesso!")
        
    else:
        print("Não foi possível encontrar o CPF informado")

def list_users():
    exists_users = len(bank.users) > 0
    if exists_users:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        
        for user in bank.users:
            print(user["name"])
            print(f"\tCPF: {user["cpf"]}")
            print(f"\tData de Nascimento: {user["birthdate"]}")
            print(f"\tEndereço: {user["address"]}\n")

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    else:
        print("Não há nenhum usuário cadastrado")

def list_accounts():
    exists_accounts = len(bank.accounts) > 0
    if exists_accounts:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        
        for account in bank.accounts:
            print(account["user"])
            print(f"\tAgência: {account["agency"]}")
            print(f"\tNúmero da conta: {account["account_number"]}")

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    else:
        print("Não há nenhuma conta cadastrada")

def main():
    while True:
        print("\n<<<<<<<<<<<<<< MENU >>>>>>>>>>>>>>")
        print("Escolha uma das operações abaixo:")

        options = {
            "1": "Depositar",
            "2": "Sacar",
            "3": "Ver Saldo",
            "4": "Extrato",
            "5": "Criar Usuário",
            "6": "Criar Conta Corrente",
            "7": "Listar Usuários",
            "8": "Listar Contas Corrente",
            "0": "Sair",
        }

        for digit, option in options.items():
            print(f"[{digit}] - {option}")

        option_pick = input("Insira o dígito referente a operação: ")

        if option_pick in options:
            option = options[option_pick]
            print(f"Você escolheu a operação: {option}")

            if option == "Depositar":
                try:
                    deposit_value = float(input("Insira o valor a ser depositado:\n\t↳ R$ "))
                    deposit_message = deposit(deposit_value)
                    print(deposit_message)
                    
                except:
                    print("Não foi possível realizar o depósito!")
                
                finally:
                    input("Pressione [Enter] para continuar...")

            if option == "Sacar":
                if bank.is_allow_withdrawal():
                    try:
                        withdrawal_value = float(input("Insira o valor a ser sacado:\n\t↳ R$ "))

                        if withdrawal_value > bank.WITHDRAWAL_VALUE_LIMIT:
                            print("Valor inserido ultrapassa o limite de R$ 500.00!")
                            raise

                        withdrawal_message = withdrawal(value=withdrawal_value)
                        
                        print(withdrawal_message)
                    
                    except:
                        print("Não foi possível realizar o saque!")
                    
                    finally:
                        input("Pressione [Enter] para continuar...")

                else:
                    print("Já foi realizado o limite de saques diário")
                    input("Pressione [Enter] para continuar...")
            
            if option == "Ver Saldo":
                print(f"Seu saldo é: R$ {bank.balance:.2f}")
                input("Pressione [Enter] para continuar...")

            if option == "Extrato":
                current_balance = bank.balance
                transactions = bank.transactions
                extract(current_balance, transactions=transactions)
                input("Pressione [Enter] para continuar...")

            if option == "Criar Usuário":
                print("Para prosseguir informe seus dados pessoais a seguir")
                name = input("Nome completo: ")
                birthdate = input("Data de nascimento separada por barras (dia/mês/ano): ")
                cpf = input("CPF (apenas os números): ")

                if find_user(cpf):
                    print("usuário já cadastrado com esse CPF informado")
                else:
                    print("\nOk! Agora informe os dados de sua localidade")
                    street = input("Rua: ")
                    street_number = input("Número da residência: ")
                    neighborhood = input("Bairro: ")
                    city = input("Cidade: ")
                    state = input("Sigla do estado (UF): ")
                    address = f"{street}, {street_number} - {neighborhood} - {city}/{state}"

                    create_user({
                        "name": name,
                        "birthdate": birthdate,
                        "cpf": cpf,
                        "address": address,
                    })
                
                input("Pressione [Enter] para continuar... \n")
                    
            if option == "Criar Conta Corrente":
                user_cpf = input("Insira um CPF (apenas os números) de um usuário válido: ")
                create_account(user_cpf)
                input("Pressione [Enter] para continuar...\n")

            if option == "Listar Usuários":
                list_users()
                input("Pressione [Enter] para continuar...\n")

            if option == "Listar Contas Corrente":
                list_accounts()
                input("Pressione [Enter] para continuar...\n")

            if option == "Sair":
                print("Agradecemos sua presença por aqui. Até logo!")
                break

        else:
            print("Operação inválida! Por favor, insira o número válido a operação")
            input("Pressione [Enter] para continuar...\n")

main()
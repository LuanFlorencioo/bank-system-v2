import inquirer


def confirm_choice(choice) -> bool:
    confirm = inquirer.list_input(
        message=f"Você escolheu a opção de {choice}. Deseja continuar?",
        choices=["Sim", "Não"],
    )

    return confirm == "Sim"

import textwrap


def menu():
    menu = """\n
    --------------MENU-------------
    [1]\tDepositar
    [2]\tSacar
    [3]\tExtrato
    [4]\tNova Conta
    [5]\tListar contas
    [6]\tNovo Usuário
    [7]\tSair
=> """
    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n Depósito Realizado com Sucesso!")
    else:
        print("\n Operação Inválida, Informe Valor Válido!")
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n Você não tem Saldo Suficiente!")
    elif excedeu_limite:
        print("\n Você não tem Limite Suficiente!")
    elif excedeu_saques:
        print("\n Você Excedeu o limite de Saques!")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n Saque Realizado com sucesso!")
    else:
        print("\n Operação Inválida, Informe Valor Válido!")
    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    print("\n -------------EXTRATO------------")
    print("Sem Movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("___________________________________")


def criar_usuario(usuarios):
    cpf = input("Informe o Núero do CPF, Apenas Números, Ex. 12312312312: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n Usuário já Existe, Tente Outro CPF!")
        return

    nome = input("Nome Completo: ")
    data_nascimento = input("Data de Nascimento, Ex. dd-mm-aaaa: ")
    endereco = input("Endereço Completo, Ex. Logradouro, 000 - Bairro - cidade/Estado(Sigla): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("\n--- Novo Cliente Criado! ---")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n--- Nova Conta Criada! ---")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\nUsuário não encontrado! Crie um usuário antes de vincular uma conta.")
    return None


def listar_contas(contas):
    if not contas:
        print("\nNenhuma conta cadastrada.")
        return
    
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("-" * 50)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        try:
            if opcao == "1":
                if not contas:
                    print("\nCrie um usuário e uma conta antes de depositar.")
                    continue
                
                valor = float(input("Valor do Depósito: "))
                saldo, extrato = depositar(saldo, valor, extrato)

            elif opcao == "2":
                if not contas:
                    print("\nCrie um usuário e uma conta antes de sacar.")
                    continue

                valor = float(input("Valor do saque: "))
                saldo, extrato, numero_saques = sacar(
                    saldo=saldo,
                    valor=valor,
                    extrato=extrato,
                    limite=limite,
                    numero_saques=numero_saques,
                    limite_saques=LIMITE_SAQUES,
                )

            elif opcao == "3":
                if not contas:
                    print("\nCrie um usuário e uma conta antes de ver o extrato.")
                    continue
                
                exibir_extrato(saldo, extrato=extrato)

            elif opcao == "4":
                if not usuarios:
                    print("\nCrie um usuário antes de criar uma conta.")
                    continue

                numero_conta = len(contas) + 1
                conta = criar_conta(AGENCIA, numero_conta, usuarios)

                if conta:
                    contas.append(conta)

            elif opcao == "5":
                listar_contas(contas)

            elif opcao == "6":
                criar_usuario(usuarios)

            elif opcao == "7":
                break

            else:
                print("\nOpção Inválida, por favor selecione novamente a operação desejada.")

        except ValueError:
            print("\nOperação inválida! Por favor, informe um valor numérico.")


main()

def soma(a, b):
    # Somar dois números
    return a + b

def subtrai(a, b):
    # Subtrair dois números
    return a - b

def multiplica(a, b):
    # Multiplicar dois números
    return a * b

def divide(a, b):
    # Dividir dois números, verificando se o divisor não é zero
    if b == 0:
        return "Erro: divisão por zero"
    return a / b

# Loop principal para interagir com o utilizador
while True:
  
    print("Escolha a operação:")
    print("1 - Soma (+)")
    print("2 - Subtração (-)")
    print("3 - Multiplicação (*)")
    print("4 - Divisão (/)")
    print("5 - Sair")
    
    # Recebe a escolha do usuário
    escolha = input("Digite o número da operação desejada: ")
    
    if escolha == "5":
        # Encerra o programa se o usuário escolher sair
        print("Encerrando a calculadora.")
        break
    
    # Recebe os números do usuário
    num1 = float(input("Digite o primeiro número: "))
    num2 = float(input("Digite o segundo número: "))
    
    # Executa a operação escolhida
    if escolha == "1":
        print("Resultado:", int(soma(num1, num2)))
    elif escolha == "2":
        print("Resultado:", int(subtrai(num1, num2)))
    elif escolha == "3":
        print("Resultado:", int(multiplica(num1, num2)))
    elif escolha == "4":
        print("Resultado:", divide(num1, num2))
    else:
        # Mensagem para opção inválida
        print("Opção inválida. Tente novamente.")
import random

print("Bem-vindo ao number guesser")
print("O pc escolheu um número entre 1 e 100.")
print("Tente adivinhar! Escreva apenas números inteiros nesse intervalo.")

numero_secreto = random.randint(1, 100)
tentativas = 0

while True:
    try:
        palpite = int(input("Digite o seu palpite (1 a 100): "))
        if palpite < 1 or palpite > 100:
            print("Por favor, digite um número dentro  de 1 a 100.")
            continue
        tentativas += 1
        if palpite < numero_secreto:
            print("Muito baixo! Tente novamente.")
        elif palpite > numero_secreto:
            print("Muito alto! Tente novamente.")
        else:
            print(f"Parabéns! Acertou o número {numero_secreto} em {tentativas} tentativas.")
            break
    except ValueError:
        print("Entrada inválida. Por favor, digite apenas números inteiros.")
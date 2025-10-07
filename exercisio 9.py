def calcular_imc(peso, altura):
    """
    Calcula o Índice de Massa Corporal (IMC).

    Args:
        peso (float): Peso em quilogramas.
        altura (float): Altura em metros.

    Returns:
        float: Valor do IMC calculado.
    """
    return peso / (altura ** 2)

def classificar_imc(imc):
    """
    Classifica o valor do IMC de acordo com faixas estabelecidas.

    Args:
        imc (float): Valor do IMC.

    Returns:
        str: Classificação correspondente ao IMC.
    """
    if imc < 18.5:
        return "Abaixo do peso"
    elif imc < 25:
        return "Peso normal"
    elif imc < 30:
        return "Excesso de peso"
    else:
        return "Obesidade"

print("Calculadora de IMC")
print("Por favor, insira os valores pedidos.")
print("O peso deve estar em quilogramas (kg) e a altura em metros (m). Exemplo: peso=70.5, altura=1.75")
while True:
    try:
        peso = float(input("Peso (kg): "))
        if peso <= 0:
            print("Por favor, introduza um valor de peso válido e maior que zero.")
            continue
        altura = float(input("Altura (m): "))
        if altura <= 0 or altura > 3:
            print("Por favor, introduza uma altura válida (maior que zero e menor que 3 metros).")
            continue
        break
    except ValueError:
        print("Entrada inválida. Utilize apenas números, por favor.")

imc = calcular_imc(peso, altura)
print(f"IMC: {imc:.2f}")
print("Classificação:", classificar_imc(imc))
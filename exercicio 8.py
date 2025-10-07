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

peso = float(input("Peso (kg): "))
altura = float(input("Altura (m): "))

print(calcular_imc.__doc__)
print(classificar_imc.__doc__)
imc = calcular_imc(peso, altura)
print(f"IMC: {imc:.2f}")
print("Classificação:", classificar_imc(imc))

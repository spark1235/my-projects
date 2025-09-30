palavras = ["computador", "sol", "maça", "livro", "biblioteca"]


maior = 0
menor = 100


for palavra in palavras:
    if len(palavra) > maior:
        maior = len(palavra)
        index_maior=palavra
    if len(palavra) < menor:
        menor = len(palavra)

print("Lista de palavras:", palavras)
print("Maior palavra:", maior, "letras", index_maior)
print("Menor palavra:", menor, "letras )")
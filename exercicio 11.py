class Animal:
    def __init__(self, nome, cor, peso):
        self.nome = nome
        self.cor = cor
        self.peso = peso

    def andar(self):
        print(f"{self.nome} está a andar.")

    def correr(self):
        print(f"{self.nome} está a correr.")

class Cao(Animal):
    def latir(self):
        print(f"{self.nome} está a latir: Au Au!")

class Animal:
    def __init__(self, nome, cor, peso):
        self.nome = nome
        self.cor = cor
        self.peso = peso

    def andar(self):
        print(f"{self.nome} está a andar.")

    def correr(self):
        print(f"{self.nome} está a correr.")

class Cao(Animal):
    def latir(self):
        print(f"{self.nome} está a latir: Au au!")

class Gato(Animal):
    def miar(self):
        print(f"{self.nome} está a miar: Miau!")

# Entrada dos dados pelo utilizador
print("Criação de um cão:")
nome_cao = input("Nome do cão: ")
cor_cao = input("Cor do cão: ")
peso_cao = float(input("Peso do cão (kg): "))
cao1 = Cao(nome_cao, cor_cao, peso_cao)

print("\nCriação de um gato:")
nome_gato = input("Nome do gato: ")
cor_gato = input("Cor do gato: ")
peso_gato = float(input("Peso do gato (kg): "))
gato1 = Gato(nome_gato, cor_gato, peso_gato)

print("\nCriação de outro cão:")
nome_cao2 = input("Nome do outro cão: ")
cor_cao2 = input("Cor do outro cão: ")
peso_cao2 = float(input("Peso do outro cão (kg): "))
cao2 = Cao(nome_cao2, cor_cao2, peso_cao2)

print("\nAções dos animais:")

# 2 ações para cada animal
cao1.andar()
cao1.latir()

gato1.correr()
gato1.miar()

cao2.andar()
cao2.correr()
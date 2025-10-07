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

class Gato(Animal):
    def miar(self):
        print(f"{self.nome} está a miar: Miau!")

print("Informações do Cão")
nome_cao = input("Nome do cão: ")
cor_cao = input("Cor do cão: ")
peso_cao = input("Peso do cão (kg): ")

cao = Cao(nome_cao, cor_cao, peso_cao)

print("\nInformações do Gato")
nome_gato = input("Nome do gato: ")
cor_gato = input("Cor do gato: ")
peso_gato = input("Peso do gato (kg): ")

gato = Gato(nome_gato, cor_gato, peso_gato)

print("\nAções do cão:")
cao.andar()
cao.correr()
cao.latir()

print("\nAções do gato:")
gato.andar()
gato.correr()
gato.miar()
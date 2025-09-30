nome=input("digite seu nome:")
sexo=input("digite seu sexo:(M/F):")
altura=float(input("digite sua altura(exemplo 1.64):"))

if sexo == "M":
    if altura >= 1.74:
        print("O", nome, "é alto.")
    else:
        print("O", nome, "é baixo.")
elif sexo == "F":
    if altura >= 1.64:
        print("A", nome, "é alta.")
    else:
        print("A", nome, "é baixa.")

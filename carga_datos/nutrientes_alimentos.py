import pandas


def nutrientes_alimentos():
    nutrientes = pandas.read_excel("./datos/alimentos.xlsx")

    nutrientes = nutrientes.set_index("Nombre")

    nutrientes = nutrientes.drop("Tipo de comida", axis=1)

    return nutrientes


if __name__ == "__main__":
    print(nutrientes_alimentos())

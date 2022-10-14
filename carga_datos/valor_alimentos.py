import pandas


def valor_alimentos():
    valores = pandas.read_excel("./datos/precios.xlsx")

    valores = valores.set_index("Nombre")

    return valores.to_dict()["Precio"]


if __name__ == "__main__":
    print(valor_alimentos())

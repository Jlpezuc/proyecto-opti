import pandas


def alimentos():
    alimentos = pandas.read_excel("./datos/alimentos.xlsx")
    return alimentos["Nombre"].to_list()


if __name__ == "__main__":
    print(alimentos())

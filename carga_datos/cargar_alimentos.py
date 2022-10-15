import pandas


def cargar_alimentos():
    alimentos = pandas.read_excel("./datos/qn_ni.xlsx")
    return alimentos["Nombre"].to_list()


if __name__ == "__main__":
    print(cargar_alimentos())

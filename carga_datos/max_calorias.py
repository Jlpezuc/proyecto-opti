import pandas


def max_calorias():
    valores = pandas.read_excel("./datos/mca_e_MCA_e.xlsx")

    valores = valores.set_index("Edad")

    return valores.to_dict()["Maximo (kcal)"]


if __name__ == "__main__":
    print(max_calorias())

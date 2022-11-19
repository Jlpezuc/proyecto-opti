import pandas


def min_calorias():
    valores = pandas.read_excel("./datos/mca_e_MCA_e.xlsx")

    valores = valores.set_index("Edad")

    return valores.to_dict()["Minimo (cal)"]


if __name__ == "__main__":
    print(min_calorias())

import pandas


def cant_nutrientes_alimento():
    nutrientes_alimento = pandas.read_excel(
        "./datos/qn_ni2.xlsx")
    nutrientes_alimento = nutrientes_alimento.set_index("Nombre")
    return nutrientes_alimento


if __name__ == "__main__":
    print(cant_nutrientes_alimento())
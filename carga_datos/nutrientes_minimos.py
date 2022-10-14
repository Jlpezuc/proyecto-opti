import pandas


def nutrientes_minimos():
    nutrientes_minimos = pandas.read_excel(
        "./datos/nutrientes_recomendados.xlsx")
    nutrientes_minimos = nutrientes_minimos.set_index("Edad")
    nutrientes_minimos = nutrientes_minimos.rename(columns={
        "Proteina(g)": "Proteina", "Lipidos(g)": "Lipidos", "Carbohidratos(g)": "Carbohidratos"})
    return nutrientes_minimos


if __name__ == "__main__":
    print(nutrientes_minimos())

import pandas


def nutrientes_minimos():
    nutrientes_minimos = pandas.read_excel(
        "./datos/nutrientes_recomendados.xlsx")
    nutrientes_minimos = nutrientes_minimos.drop('Edad', axis=1)
    # nutrientes_minimos = nutrientes_minimos.to_dict('dict')
    for _ in range(0, 6):
        nutrientes_minimos.loc[nutrientes_minimos.shape[0]] = [
            None, None, None]
    nutrientes_minimos = nutrientes_minimos.shift(periods=6)
    nutrientes_minimos = nutrientes_minimos.rename(columns={
        "Proteina(g)": "Proteina", "Lipidos(g)": "Lipidos", "Carbohidratos(g)": "Carbohidratos"})
    return nutrientes_minimos


if __name__ == "__main__":
    print(nutrientes_minimos())

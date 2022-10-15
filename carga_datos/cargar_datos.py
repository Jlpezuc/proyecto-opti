import pandas


def cargar_datos(filename):
    file = pandas.read_excel(f"./datos/{filename}")
    index_col = file.columns[0]
    file = file.set_index(index_col)
    return file


if __name__ == "__main__":
    print(cargar_archivo("nutrientes_recomendados.xlsx"))

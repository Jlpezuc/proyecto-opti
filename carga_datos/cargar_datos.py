import pandas


def cargar_datos(filename):
    file = pandas.read_excel(f"./datos/{filename}")
    index_col = file.columns[0]
    file = file.set_index(index_col)
    col = file.columns[0]
    return file.to_dict()[col]


def cargar_multiples_datos(filename):
    file = pandas.read_excel(f"./datos/{filename}")
    index_col = file.columns[0]
    file = file.set_index(index_col)
    return file


if __name__ == "__main__":
    print(cargar_multiples_datos("qn_ni2.xlsx"))
    # print(cargar_multiples_datos("mne_ne.xlsx"))

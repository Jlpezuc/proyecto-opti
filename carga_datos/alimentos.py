import pandas


def nutri_alimentos():
    alimentos = pandas.read_excel("./datos/alimentos.xlsx")
    return alimentos.to_dict('dict')


if __name__ == "__main__":
    print(nutri_alimentos())

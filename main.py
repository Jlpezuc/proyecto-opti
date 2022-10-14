from gurobipy import GRB, Model, quicksum


# ----------------Generamos Modelo ------------#
model = Model()
model.setParam("TimeLimit", 1800)  # Tiempo máximo en segundos

# ---------------- Conjuntos ------------------#

S_ = range(1, 38 + 1)  # Semanas en 1 año escolar
T_ = range(1, 5 + 1)  # Días de clases en 1 semana
E_ = range(6, 18 + 1)  # Edades
I_ = range(1, 137 + 1)  # Alimentos que ofrece la Junaeb
J_ = range(1, 9931 + 1)  # Numero colegios
N_ = range(1, 3 + 1)  # Tipos de macronutrientes
D_ = range(1, 3 + 1)  # Tipos de dietas

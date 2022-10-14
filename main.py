from gurobipy import GRB, Model, quicksum


# ----------------Generamos Modelo ------------#
model = Model()
model.setParam("TimeLimit", 1800)  # Tiempo máximo en segundos

# ---------------- Conjuntos ------------------#

s_ = range(1, 38 + 1)  # Semanas en 1 año escolar
t_ = range(1, 5 + 1)  # Días de clases en 1 semana
e_ = range(6, 18 + 1)  # Edades
i_ = range(1, 137 + 1)  # Alimentos que ofrece la Junaeb
j_ = range(1, 9931 + 1)  # Numero colegios
n_ = range(1, 3 + 1)  # Tipos de macronutrientes
d_ = range(1, 3 + 1)  # Tipos de dietas

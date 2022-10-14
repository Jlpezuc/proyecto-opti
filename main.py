from gurobipy import GRB, Model, quicksum


# ----------------Generamos Modelo ------------#
model = Model()
model.setParam("TimeLimit", 1800)  # Tiempo máximo en segundos

# ---------------- Conjuntos ------------------ #

s_ = range(1, 38 + 1)  # Semanas en 1 año escolar
t_ = range(1, 5 + 1)  # Días de clases en 1 semana
e_ = range(6, 18 + 1)  # Edades
i_ = range(1, 137 + 1)  # Alimentos que ofrece la Junaeb
j_ = range(1, 9931 + 1)  # Numero colegios
n_ = range(1, 3 + 1)  # Tipos de macronutrientes
d_ = range(1, 3 + 1)  # Tipos de dietas

# ---------------- Importar Parametros ----------#

presupuesto = ""
costo_gramo = ""
costo_almacenamiento = ""
min_calorias = ""
max_calorias = ""
min_macronutrientes = ""
calorias_alimento = ""
cant_nutriente_alimento = ""
cant_max_gramos_almacenaje = ""
masa_porcion_alimento = ""
cant_estudiantes_instituto = ""

# ---------------- Creación Parametros ----------#

p = {(s): presupuesto[s - 1] for s in s_}
cg = {(i): costo_gramo[i - 1] for i in i_}
cc = {(i, j): costo_almacenamiento[i - 1][j - 1] for i in i_ for j in j_}
mca = {(e): min_calorias[e - 1] for e in e_}
MCA = {(e): max_calorias[e - 1] for e in e_}
mn = {(n, e): min_macronutrientes[n - 1][e - 1] for n in n_ for e in e_}
qca = {(i): calorias_alimento[i - 1] for i in i_}
qn = {(n, i): cant_nutriente_alimento[n - 1][i - 1] for n in n_ for i in i_}
qc = {(j): cant_max_gramos_almacenaje[j - 1] for j in j_}
g = {(i): masa_porcion_alimento[i - 1] for i in i_}
qp = {(j, d): cant_estudiantes_instituto[j - 1][d - 1] for j in j_ for d in d_}
a = ""  # agregar valor
M = 1000000

# ---------------- Variables ------------------ #

# Presupuesto destinado al colegio j para la semana s
L = model.addVars(j_, s_, vtype=GRB.CONTINUOUS)
# Cantidad total de gramos del alimento i a servir en el dia t en la dieta d en el instituto j
QS = model.addVars(i_, t_, d_, j_, vtype=GRB.CONTINUOUS)
# Cantidad de gramos del alimento i que se almacena en el instituto j al final de la semana s
QA = model.addVars(i_, j_, s_, vtype=GRB.CONTINUOUS)
# Cantidad de gramos del aliemtno i que se destina al instituto j en la semana s
QN = model.addVars(i_, j_, s_, vtype=GRB.CONTINUOUS)
# 1 si se utiliza el alimento i en el dia t para la dieta d para el instituto j, 0 eoc
Y = model.addVars(i_, d_, t_, j_, s_, vtype=GRB.CONTINUOUS)

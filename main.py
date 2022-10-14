import imp
from gurobipy import GRB, Model, quicksum
from carga_datos import nutrientes_minimos, alimentos, nutrientes_alimentos, valor_alimentos

# ----------------Generamos Modelo ------------#
model = Model()
model.setParam("TimeLimit", 1800)  # Tiempo máximo en segundos

# ---------------- Conjuntos ------------------ #

s_ = range(1, 38 + 1)  # Semanas en 1 año escolar
t_ = range(1, 5 + 1)  # Días de clases en 1 semana
e_ = range(6, 18 + 1)  # Edades
i_ = alimentos()  # Alimentos que ofrece la Junaeb
j_ = range(1, 9931 + 1)  # Numero colegios
n_ = {"Proteina", "Lipidos", "Carbohidratos"}  # Tipos de macronutrientes
d_ = range(1, 3 + 1)  # Tipos de dietas

# ---------------- Importar Parametros ----------#

presupuesto = ""
costo_gramo = valor_alimentos()
min_calorias = ""
max_calorias = ""
min_macronutrientes = nutrientes_minimos()
calorias_alimento = ""
cant_nutriente_alimento = nutrientes_alimentos()
cant_max_gramos_almacenaje = ""
masa_porcion_alimento = ""
cant_estudiantes_instituto = ""

# ---------------- Creación Parametros ----------#

p = {(s): presupuesto[s - 1] for s in s_}
cg = {(i): costo_gramo[i - 1] for i in i_}
cc = 0  # asignar valor
mca = {(e): min_calorias[e - 1] for e in e_}
MCA = {(e): max_calorias[e - 1] for e in e_}
mn = {(n, e): min_macronutrientes[n][e] for n in n_ for e in e_}
qca = {(i): calorias_alimento[i - 1] for i in i_}
qn = {(n, i): cant_nutriente_alimento[n - 1][i - 1] for n in n_ for i in i_}
qc = {(j): cant_max_gramos_almacenaje[j - 1] for j in j_}
g = {(i): masa_porcion_alimento[i - 1] for i in i_}
qp = {(j, d): cant_estudiantes_instituto[j - 1][d - 1] for j in j_ for d in d_}
a = ""  # agregar valor
M = 1000000

# ---------------- Variables ------------------ #

# Presupuesto destinado al colegio j para la semana s
L = model.addVars(j_, s_, vtype=GRB.INTEGER)
# Cantidad total de gramos del alimento i a servir en el dia t en la dieta d en el instituto j
QS = model.addVars(i_, t_, d_, j_, vtype=GRB.CONTINUOUS)
# Cantidad de gramos del alimento i que se almacena en el instituto j al final de la semana s
QA = model.addVars(i_, j_, s_, vtype=GRB.CONTINUOUS)
# Cantidad de gramos del aliemtno i que se destina al instituto j en la semana s
QN = model.addVars(i_, j_, s_, vtype=GRB.CONTINUOUS)
# 1 si se utiliza el alimento i en el dia t para la dieta d para el instituto j, 0 eoc
Y = model.addVars(i_, d_, t_, j_, s_, vtype=GRB.BINARY)
# variable auxiliar mu
MU = model.addVars(vtype=GRB.CONTINUOUS)
Z = model.addVars(t_, j_, vtype=GRB.BINARY)

# ---------------- Creacion de Restricciones ------------------ #
# R1
model.addConstrs((Y[i, d, t, j, s] <= QS[i, d, t, j] *
                 M for i in i_ for d in d_ for t in t_ for j in j_ for s in s_), name="R1")

# R2
model.addConstrs((quicksum(quicksum(quicksum(Y[i, d, t, j, s] * a + cg[i][i] * QS[i, d, t, j] * qp[i, d][s] for d in d_)
                 for t in t_) + cc[i, j] * QA[i, j, s] for i in i_) <= L[j, s] for j in j_ for s in s_), name="R2")

# R3
model.addConstrs((quicksum(L[j, s] for j in j_) < p[s] for s in s_), name="R3")

# R4
model.addConstrs((quicksum(Y[i, d, t, j, s] for t in t_) <=
                 2 for i in i_ for j in j_ for s in s_ for d in d_), name="R4")

# R5
model.addConstrs((quicksum(Y[i, d, t, j, s] for t in t_) + quicksum(Y[i, d, t, j, s] for t in t_)
                 <= 3 for d in d_ for i in i_ for j in j_ for s in s_), name="R5")

# R6
model.addConstrs(
    (Y[i, d, t, j, s] + Y[i, d, t, j, s] + Y[i, d, t, j, s] <= 1 for d in d_ for i in i_ for t in t_ for j in j_ for s in s_), name="R6")

# R7
model.addConstrs((mca[e] <= quicksum(Y[i, d, t, j, s] * g[i] * qca[i] for i in i_)
                 for t in t_ for j in j_ for d in d_ for e in e_ for s in s_), name="R7")
model.addConstrs((quicksum(Y[i, d, t, j, s] * g[i] * qca[i] for i in i_) <= MCA[e]
                 for t in t_ for j in j_ for d in d_ for e in e_ for s in s_), name="R7")

# R8
model.addConstrs((mn[n, e] <= quicksum(Y[i, d, t, j, s] * g[i] * qca[i] for i in i_)
                 for e in e_ for d in d_ for t in t_ for n in n_ for j in j_ for s in s_), name="R8")

# R9
model.addConstrs((quicksum(Y[i, d, t, j, s] for i in i_) >=
                 2 for d in d_ for t in t_ for j in j_ for s in s_), name="R9")

# R10
model.addConstrs((quicksum(QA[i, j, s] for i in i_) <=
                 qc[j] for s in s_ for j in j_), name="R10")

# R11
model.addConstrs((QA[i, j, s - 1] + QN[i, j, s] == QA[i, j, s] + quicksum(quicksum(QS[i, d, t, j] for t in t_)
                 for d in d_) for i in i_ for j in j_ for s in s_[1:]), name="R11")

# R12
model.addConstrs((QN[i, j, s] == QA[i, j, s] + quicksum(quicksum(QS[i, d, t, j] for t in t_)
                 for d in d_) for i in i_ for j in j_ for s in s_), name="R12")

# R13
model.addConstrs((MU <= Y[i, d, t, j, s] * g[i] * qca[i]
                 for i in i_ for j in j_ for s in s_ for d in d_ for t in t_), name="R13")

# ---------------- Naturaleza de las variables ------------------ #
model.addConstrs((L[j, s] >= 0 for s in s_ for j in j_), name="R14")

# ---------------- Creacion de Funcion Objetivo ------------------ #
# model.setObjective(quicksum(quicksum(quicksum(quicksum(
#     Y[i, t, d, j] * g[i] * qca[i] for i in i_) for t in t_) for d in d_) for j in j_) / len(t_), GRB.MAXIMIZE)
model.setObjective(MU, GRB.MAXIMIZE)

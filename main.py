import imp
from gurobipy import GRB, Model, quicksum
from carga_datos.cargar_datos import cargar_datos, cargar_multiples_datos
from carga_datos.max_calorias import max_calorias
from carga_datos.min_calorias import min_calorias
from carga_datos.cargar_alimentos import cargar_alimentos
# ----------------Generamos Modelo ------------#
model = Model()
model.setParam("TimeLimit", 1800)  # Tiempo máximo en segundos

# ---------------- Conjuntos ------------------ #

s_ = range(1, 38 + 1)  # Semanas en 1 año escolar
t_ = range(1, 5 + 1)  # Días de clases en 1 semana
e_ = range(6, 18 + 1)  # Edades
i_ = cargar_alimentos()  # Alimentos que ofrece la Junaeb
j_ = range(1, 500 + 1)  # Numero colegios
n_ = {"Proteina", "Lipidos", "Carbohidratos"}  # Tipos de macronutrientes
d_ = range(1, 3 + 1)  # Tipos de dietas

# ---------------- Importar Parametros ----------#

presupuesto = cargar_datos("p_s.xlsx")
costo_gramo = cargar_datos("cg_i.xlsx")
min_calorias = min_calorias()
max_calorias = max_calorias()
min_macronutrientes = cargar_multiples_datos("mne_ne.xlsx")
calorias_alimento = cargar_datos("qca.xlsx")
cant_nutriente_alimento = cargar_multiples_datos("qn_ni.xlsx")
# masa_porcion_alimento = cargar_datos()
cant_estudiantes_instituto = cargar_multiples_datos("qp_jd.xlsx")

# ---------------- Creación Parametros ----------#

p = {(s): presupuesto[s] for s in s_}
cg = {(i): costo_gramo[i] for i in i_}
cc = 76.76
mca = {(e): min_calorias[e] for e in e_}
MCA = {(e): max_calorias[e] for e in e_}
mn = {(n, e): min_macronutrientes[n][e] for n in n_ for e in e_}
qca = {(i): calorias_alimento[i] for i in i_}
qn = {(n, i): cant_nutriente_alimento[n][i] for n in n_ for i in i_}
qc = 80000
# g = {(i): masa_porcion_alimento[i - 1] for i in i_}
qp = {(d, j): cant_estudiantes_instituto[d][j] for j in j_ for d in d_}
a = 327
M = 1000000

# ---------------- Variables ------------------ #

# Presupuesto destinado al colegio j para la semana s
L = model.addVars(j_, s_, vtype=GRB.INTEGER)
# Cantidad total de gramos del alimento i a servir en el dia t en la dieta d en el instituto j
QS = model.addVars(i_, d_, t_, j_, s_, vtype=GRB.CONTINUOUS)
# Cantidad de gramos del alimento i que se almacena en el instituto j al final de la semana s
QA = model.addVars(i_, j_, s_, vtype=GRB.CONTINUOUS)
# Cantidad de gramos del aliemtno i que se destina al instituto j en la semana s
QN = model.addVars(i_, j_, s_, vtype=GRB.CONTINUOUS)
# 1 si se utiliza el alimento i en el dia t para la dieta d para el instituto j, 0 eoc
Y = model.addVars(i_, d_, t_, j_, s_, vtype=GRB.BINARY)
# variable auxiliar mu
MU = model.addVar(vtype=GRB.CONTINUOUS)
Z = model.addVars(t_, j_, vtype=GRB.BINARY)

# ---------------- Creacion de Restricciones ------------------ #
# R1
model.addConstrs((Y[i, d, t, j, s] <= QS[i, d, t, j, s]
                for i in i_ for d in d_ for t in t_ for j in j_ for s in s_), name="R1")

# R2
model.addConstrs((quicksum(quicksum(quicksum(Y[i, d, t, j, s] * a + cg[i] * QS[i, d, t, j, s] * qp[d, j] for d in d_)
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
model.addConstrs((mca[e] <= quicksum(QS[i, d, t, j, s] * qca[i] for i in i_)
                 for t in t_ for j in j_ for d in d_ for e in e_ for s in s_), name="R7")
model.addConstrs((quicksum(QS[i, d, t, j, s] * qca[i] for i in i_) <= MCA[e]
                 for t in t_ for j in j_ for d in d_ for e in e_ for s in s_), name="R7")

# R8
model.addConstrs((mn[n, e] <= quicksum(QS[i, d, t, j, s] * qca[i] for i in i_)
                 for e in e_ for d in d_ for t in t_ for n in n_ for j in j_ for s in s_), name="R8")

# R9
model.addConstrs((quicksum(Y[i, d, t, j, s] for i in i_) >=
                 2 for d in d_ for t in t_ for j in j_ for s in s_), name="R9")

# R10
model.addConstrs((QA[i, j, s] <= M * Z[s, j]
                 for i in i_ for j in j_ for s in s_), name="R10") 

# R11
model.addConstrs((quicksum(QA[i, j, s] for i in i_) <=
                 qc[j] for s in s_ for j in j_), name="R11")

# R12
model.addConstrs((QA[i, j, s - 1] + QN[i, j, s] == QA[i, j, s] + quicksum(quicksum(QS[i, d, t, j, s] for t in t_)
                 for d in d_) for i in i_ for j in j_ for s in s_[1:]), name="R12")

# R13
model.addConstrs((QN[i, j, s] == QA[i, j, s] + quicksum(quicksum(QS[i, d, t, j, s] for t in t_)
                 for d in d_) for i in i_ for j in j_ for s in s_), name="R13")

# R14
model.addConstrs((MU <= QS[i, d, t, j, s] * qca[i]
                 for i in i_ for j in j_ for d in d_ for t in t_ for s in s_), name="R14")


# ---------------- Naturaleza de las variables ------------------ #
model.addConstrs((L[j, s] >= 0 for s in s_ for j in j_), name="R15")

# ---------------- Creacion de Funcion Objetivo ------------------ #
# model.setObjective(quicksum(quicksum(quicksum(quicksum(
#     Y[i, t, d, j] * g[i] * qca[i] for i in i_) for t in t_) for d in d_) for j in j_) / len(t_), GRB.MAXIMIZE)
model.setObjective(MU, GRB.MAXIMIZE)

# Optimizamos
model.optimize()

# Veremos qué restricciones están activas
print("\n"+"-"*9+" Restricciones Activas "+"-"*9)
for constr in model.getConstrs():
    if constr.getAttr("slack") == 0:
        print(f"La restriccion {constr} está activa")

# Veamos todas las soluciones posibles
model.printAttr("X")

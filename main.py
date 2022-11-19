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

s_ = range(1, 19 + 1)  # Semanas en 1 año escolar
t_ = range(1, 5 + 1)  # Días de clases en 1 semana
i_ = cargar_alimentos()  # Alimentos que ofrece la Junaeb
j_ = range(1, 70 + 1)  # Numero colegios  # 500
n_ = {"Proteina", "Lipidos", "Carbohidratos"}  # Tipos de macronutrientes

# ---------------- Importar Parametros ----------#

presupuesto = cargar_datos("p_s.xlsx")
costo_gramo = cargar_datos("cg_i.xlsx")
min_calorias = min_calorias()
max_calorias = max_calorias()
min_macronutrientes = {"Proteina": 0.25,
                       "Lipidos": 0.25, "Carbohidratos": 0.45}
calorias_alimento = cargar_datos("qca.xlsx")
cant_nutriente_alimento = cargar_multiples_datos("qn_ni.xlsx")
cant_estudiantes_instituto = cargar_datos("qp_jd.xlsx")

# ---------------- Creación Parametros ----------#

p = 17769663842
cg = {(i): costo_gramo[i] for i in i_}
cc = 77
mca = 1000000
MCA = 1608000
mn = {(n): min_macronutrientes[n] for n in n_}
qca = {(i): calorias_alimento[i] for i in i_}
qn = {(n, i): cant_nutriente_alimento[n][i] for n in n_ for i in i_}
qc = 80000
qp = {(j): cant_estudiantes_instituto[j] for j in j_}
a = 327
M_1 = 10**6
M_2 = 10**2

# ---------------- Variables ------------------ #

# Presupuesto destinado al colegio j para la semana s
L = model.addVars(j_, s_, vtype=GRB.INTEGER)
# Cantidad total de gramos del alimento i a servir en el dia t en la dieta d en el instituto j
QS = model.addVars(i_, t_, j_, s_, vtype=GRB.CONTINUOUS)
# Cantidad de gramos del alimento i que se almacena en el instituto j al final de la semana s
QA = model.addVars(i_, j_, s_, vtype=GRB.CONTINUOUS)
# Cantidad de gramos del aliemtno i que se destina al instituto j en la semana s
QN = model.addVars(i_, j_, s_, vtype=GRB.CONTINUOUS)
# 1 si se utiliza el alimento i en el dia t para la dieta d para el instituto j, 0 eoc
Y = model.addVars(i_, t_, j_, s_, vtype=GRB.BINARY)
# variable auxiliar mu
MU = model.addVar(vtype=GRB.CONTINUOUS)
# 1 si se guarda alimento i en colegio j, 0 eoc.
Z = model.addVars(s_, j_, vtype=GRB.BINARY)

# ---------------- Creacion de Restricciones ------------------ #
# R1
model.addConstrs((M*Y[i, t, j, s] >= QS[i, t, j, s]
                  for i in i_ for t in t_ for j in j_ for s in s_), name="R1")

# R2
model.addConstrs((quicksum(quicksum(Y[i, t, j, s] * a + cg[i] * QS[i, t, j, s]
                 for t in t_) + cc * Z[s, j] for i in i_) <= L[j, s] for j in j_ for s in s_), name="R2")

# R3
model.addConstrs((quicksum(L[j, s] for j in j_) <= p for s in s_), name="R3")

# R4
model.addConstrs((quicksum(Y[i, t, j, s] for t in t_) <=
                 2 for i in i_ for j in j_ for s in s_), name="R4")

# R5
model.addConstrs((quicksum(Y[i, t, j, s] for t in t_) + quicksum(Y[i, t, j, s - 1] for t in t_)
                 <= 3 for i in i_ for j in j_ for s in s_[1:]), name="R5")

# R6
model.addConstrs(
    (Y[i, t, j, s] + Y[i, t, j, s - 1] + Y[i, t, j, s - 2] <= 1 for i in i_
     for t in t_ for j in j_ for s in s_[2:]), name="R6")

# R7
model.addConstrs((mca <= quicksum(QS[i, t, j, s] * qca[i] for i in i_)
                 for t in t_ for j in j_ for s in s_), name="R7_1")
model.addConstrs((quicksum(QS[i, t, j, s] * qca[i] for i in i_) <= MCA
                 for t in t_ for j in j_ for s in s_), name="R7_2")

# R8
model.addConstrs((quicksum(Y[i, t, j, s] for i in i_) >=
                 5 for t in t_ for j in j_ for s in s_), name="R8")

# R9
model.addConstrs((QA[i, j, s] <= M_2 * Z[s, j]
                 for i in i_ for j in j_ for s in s_), name="R9")

# R10
model.addConstrs((quicksum(QA[i, j, s] for i in i_) <=
                 qc for s in s_ for j in j_), name="R10")

# R11
model.addConstrs((QA[i, j, s - 1] + QN[i, j, s] == QA[i, j, s] + quicksum(QS[i, t, j, s]
                                                                          for t in t_) for i in i_ for j in j_ for s in s_[1:]), name="R11")

# R12
model.addConstrs((QN[i, j, s_[0]] == QA[i, j, s_[0]] + quicksum(QS[i, t, j, s_[0]] for t in t_)
                  for i in i_ for j in j_), name="R12")


# R13
model.addConstrs((MU <= quicksum(QS[i, t, j, s] * qca[i]
                 for i in i_) for j in j_ for t in t_ for s in s_), name="R13")

# R15
model.addConstrs((mn[n] * mca <= quicksum(qn[n, i] * QS[i, t, j, s] for i in i_)
                  for n in n_ for t in t_ for j in j_ for s in s_), name="R15")

# ---------------- Naturaleza de las variables ------------------ #
model.addConstrs((L[j, s] >= 0 for s in s_ for j in j_), name="R14_1")
model.addConstrs(
    (QA[i, j, s] >= 0 for s in s_ for j in j_ for i in i_), name="R14_2")
model.addConstrs(
    (QS[i, t, j, s] >= 0 for s in s_ for j in j_ for i in i_ for t in t_), name="R14_3")
model.addConstrs(
    (QN[i, j, s] >= 0 for s in s_ for j in j_ for i in i_), name="R14_4")
model.addConstr((MU >= 0), name="R14_5")

# ---------------- Creacion de Funcion Objetivo ------------------ #
# model.setObjective(quicksum(quicksum(quicksum(quicksum(
#     Y[i, t, d, j] * g[i] * qca[i] for i in i_) for t in t_) for d in d_) for j in j_) / len(t_), GRB.MAXIMIZE)
model.setObjective(MU, GRB.MAXIMIZE)

# Optimizamos
model.optimize()
valor_objetivo = model.ObjVal
print(
    f"El máximo de la cota inferior de calorías que puede recibir una persona es de: {round(valor_objetivo / 1000)} kcal")


# Escribimos los archivos
with open("resultados/resultados_L.csv", "w") as archivo:
    archivo.write("Variable L: j, s")
    for j in j_:
        for s in s_:
            archivo.write(f"\n{int(L[j, s].x)}, {j}, {s}")

with open("resultados/resultados_QS.csv", "w") as archivo:
    archivo.write("Variable QS: i, t, j, s")
    for i in i_:
        for t in t_:
            for j in j_:
                for s in s_:
                    archivo.write(
                        f"\n{int(QS[i, t, j, s].x)}, {i}, {t}, {j}, {s}")

with open("resultados/resultados_QA.csv", "w") as archivo:
    archivo.write("Variable QS: i, j, s")
    for i in i_:
        for j in j_:
            for s in s_:
                archivo.write(f"\n{int(QA[i, j, s].x)}, {i}, {j}, {s}")

with open("resultados/resultados_QN.csv", "w") as archivo:
    archivo.write("Variable QN: i, j, s")
    for i in i_:
        for j in j_:
            for s in s_:
                archivo.write(f"\n{int(QN[i, j, s].x)}, {i}, {j}, {s}")

with open("resultados/resultados_Y.csv", "w") as archivo:
    archivo.write("Variable Y: i, t, j, s")
    for i in i_:
        for t in t_:
            for j in j_:
                for s in s_:
                    archivo.write(
                        f"\n{int(Y[i, t, j, s].x)}, {i}, {t}, {j}, {s}")

with open("resultados/resultados_Z.csv", "w") as archivo:
    archivo.write("Variable Z: s, j")
    for s in s_:
        for j in j_:
            archivo.write(f"\n{int(Z[s, j].x)}, {s}, {j}")

with open("resultados/resultados_MU.csv", "w") as archivo:
    archivo.write("Variable MU")
    archivo.write(f"\n{int(MU.x)}")

with open("resultados/presupuesto_semestral.csv", "w") as archivo:
    archivo.write("Instituto: Presupuesto")
    for j in j_:
        s_s = 0
        for s in s_:
            s_s += int(L[j, s].x)
        archivo.write(f"\n{j},{s_s}")


suma_cal_por_alimento = ""
suma_gramos_por_alimento = ""
for j in j_:
    for s in s_:
        for t in t_:
            for i in i_:
                if int(QS[i, t, j, s].x) != 0:
                    x = f"\nEn la semana {s} en el día {t} para el instituto {j} se consumen {int(int(QS[i, t, j, s].x) * qca[i])} cal del alimento {i}"
                    y = f"\nEn la semana {s} en el día {t} para el instituto {j} se consumen {int(QS[i, t, j, s].x)} gramos del alimento {i}"
                    suma_cal_por_alimento += x
                    suma_gramos_por_alimento += y


with open("resultados/suma_calorias_por_alimento.csv", "w") as archivo:
    archivo.write(suma_cal_por_alimento)

with open("resultados/suma_gramos_por_alimento.csv", "w") as archivo:
    archivo.write(suma_gramos_por_alimento)

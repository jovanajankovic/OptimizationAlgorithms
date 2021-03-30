import numpy as np
import math
import random

A = np.array([1.0, 5.0, 1.0])
B = np.array([3.0, 2.0, 0.0])
C = np.array([5.0, 7.0, 1.0])
D = np.array([6.0, 3.0, 3.0])

velicina_populacije = 60
dimenzija = 6
w = 0.729
c1 = 1.494
c2 = 1.494
v = np.array([0.0]*dimenzija)
v_max = 0.2
itot = 6000

def distanca(x1, y1, z1, x2, y2, z2):
    return math.sqrt(((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2))

def cost_f(x1, y1, z1, x2, y2, z2):
    suma = 0.0
    suma += distanca(A[0], A[1], A[2], x1, y1, z1)
    suma += distanca(B[0], B[1], B[2], x1, y1, z1)
    suma += distanca(x1, y1, z1, x2, y2, z2)
    suma += distanca(x2, y2, z2, C[0], C[1], C[2])
    suma += distanca(x2, y2, z2, D[0], D[1], D[2])
    return suma

populacija = []
pbest_vektor = []
pbest = np.array([0.0] * velicina_populacije)

print("Algoritam je zapoceo sa radom...")
for i in range(velicina_populacije):
    populacija.append(np.array([random.uniform(0, 7), random.uniform(0, 7), random.uniform(0, 7), random.uniform(0, 7), random.uniform(2, 7),random.uniform(0, 7)]))
    pbest_vektor.append(np.array([random.uniform(0, 7), random.uniform(0, 7), random.uniform(0, 7), random.uniform(0, 7), random.uniform(2, 7),random.uniform(0, 7)]))
    pbest[i] = cost_f(populacija[i][0], populacija[i][1], populacija[i][2], populacija[i][3], populacija[i][4],populacija[i][5])

gbest_vektor = np.array([random.uniform(0, 7), random.uniform(0, 7), random.uniform(0, 7), random.uniform(0, 7), random.uniform(0, 7),random.uniform(0, 7)])
gbest = cost_f(gbest_vektor[0], gbest_vektor[1], gbest_vektor[2], gbest_vektor[3], gbest_vektor[4], gbest_vektor[5])

for i in range(itot):
    for j in range(velicina_populacije):
        trenutna_duzina = cost_f(populacija[j][0], populacija[j][1], populacija[j][2], populacija[j][3],populacija[j][4], populacija[j][5])
        if trenutna_duzina <= pbest[j]:
            for k in range(dimenzija):
                pbest_vektor[j][k] = populacija[j][k]
            pbest[j] = trenutna_duzina
            if trenutna_duzina <= gbest:
                for k in range(dimenzija):
                    gbest_vektor[k] = populacija[j][k]
            gbest = trenutna_duzina
        for k in range(dimenzija):
            v_trenutno = w * v[k] + c1 * random.uniform(0, 1) * (pbest_vektor[j][k] - populacija[j][k]) + c2 * random.uniform(0, 1) * (gbest_vektor[k] - populacija[j][k])
            if v_trenutno > v_max:
                v[k] = v_max
            else:
                v[k] = v_trenutno
            populacija[j][k] += v[k]

print("Koordinate trazenih tacaka su: " + str(gbest_vektor[0]) + ", " + str(gbest_vektor[1]) + ", " +str(gbest_vektor[2]) + ", " + str(gbest_vektor[3]) + ", " + str(gbest_vektor[4]) + ", " + str(gbest_vektor[5]))
print("Najkraca putanja: " + str(cost_f(gbest_vektor[0], gbest_vektor[1], gbest_vektor[2], gbest_vektor[3], gbest_vektor[4], gbest_vektor[5])))
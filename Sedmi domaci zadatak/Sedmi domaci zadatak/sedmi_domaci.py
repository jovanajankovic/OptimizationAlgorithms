import numpy as np
import matplotlib.pyplot as plt
import math
import random
import copy

#niz sa velicinom fajlova iz postavke zadatka
s = np.array([173669, 275487, 1197613, 1549805, 502334, 217684, 1796841, 274708,
              631252, 148665, 150254, 4784408, 344759, 440109, 4198037, 329673, 28602,
              144173, 1461469, 187895, 369313, 959307, 1482335, 2772513, 1313997, 254845,
              486167, 2667146, 264004, 297223, 94694, 1757457, 576203, 8577828, 498382,
              8478177, 123575, 4062389, 3001419, 196884, 617991, 421056, 3017627, 131936,
              1152730, 2676649, 656678, 4519834, 201919, 56080, 2142553, 326263, 8172117,
              2304253, 4761871, 205387, 6148422, 414559, 2893305, 2158562, 465972, 304078,
              1841018, 1915571])

#inicijalizacija konstanti
broj_fajlova = 64
broj_pokretanja = 20
itot = 100000
velicina_mem = 64 * 1024 * 1024
pocetna_temp = 32 * 1024 * 1024
a = 0.95
h_min = 1
h_max = 64

#inicijalizacija promenljivih
najbolji_minimum = velicina_mem

#inicijalizacija niza
x = np.array([0] * broj_fajlova)
matrica = np.zeros((broj_pokretanja, itot))
tok_optimizacije = np.zeros((broj_pokretanja, itot))
najbolje_resenje = np.array([0] * broj_fajlova)
najbolje_resenje_za_sve = np.array([0] * broj_fajlova)
srednji_kumulativ = np.array([0] * itot)

def cost_fja(x):
    rezultat = 0
    rezultat = velicina_mem - np.matmul(x, s)
    if rezultat >= 0:
        return int(rezultat)
    else:
        return velicina_mem

print("Algoritam je zapoceo sa radom... Potrebno je da se zavrsi svih 20 pokretanja algoritma...")

for pokretanje in range(broj_pokretanja):
    temperatura = pocetna_temp
    minimum = velicina_mem
    for j in range(broj_fajlova):
        x[j] = random.randint(0, 1)
    stara = cost_fja(x)
    i = 1
    while i <= itot:
        novo_x = np.array([0]*broj_fajlova)
        novo_x = copy.deepcopy(x)
        hamming = int(((h_min - h_max) / (itot - 1)) * (i - 1) + h_max)
        for jj in range(hamming):
            pozicija = random.randint(0, 63)
            if novo_x[pozicija] == 0:
                novo_x[pozicija] = 1
            elif novo_x[pozicija] == 1:
                novo_x[pozicija] = 0
        nova = cost_fja(novo_x)
        tok_optimizacije[pokretanje][i-1] = nova
        if stara <= nova:
            if math.exp((-(nova - stara)) / temperatura) > random.uniform(0, 1):
                stara = nova
                x = copy.deepcopy(novo_x)
                if stara < minimum:
                    najbolje_resenje = copy.deepcopy(x)
                    minimum = stara
        else:
            stara = nova
            x = copy.deepcopy(novo_x)
            if stara < minimum:
                najbolje_resenje = copy.deepcopy(x)
                minimum = stara
        matrica[pokretanje][i - 1] = minimum
        i = i + 1
        temperatura = temperatura * a
    if minimum < najbolji_minimum:
        najbolje_resenje_za_sve = copy.deepcopy(najbolje_resenje)
        najbolji_minimum = minimum
    print("Zavrseno pokretanje broj " + str(pokretanje+1))

for j in range(itot):
    pomocna = 0
    for i in range(broj_pokretanja):
        pomocna = pomocna + matrica[i][j]
    pomocna = pomocna / broj_pokretanja
    srednji_kumulativ[j] = pomocna

print("Najbolje resenje za sva pokretanja - raspored fajlova je :")
print(najbolje_resenje_za_sve)
print("Najbolje resenje cost f-je u svih 20 pokretanja " + str(najbolji_minimum))

plt.figure()
for j in range(broj_pokretanja):
    plt.loglog(np.arange(0, itot, 1), matrica[j])
plt.show()

plt.figure()
plt.loglog(np.arange(0, itot, 1), srednji_kumulativ)
plt.show()
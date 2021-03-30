import matplotlib.pyplot as plt
import random
import numpy as np
import copy

#fajlovi i njihova velicina
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
velicina_memorije = 1024 * 1024 * 64
itot = 100000
broj_roditelja = 400
broj_jedinki = 2000
UKRSTANJE = 0.8
MUTACIJA = 0.1

#inicijalizacija promenljivih
najbolji_minimum = velicina_memorije
postoji = False

#inicijalizacija nizova
najbolje_resenje = np.array([0]*broj_fajlova)
najbolje_resenje_za_sve = np.array([0]*broj_fajlova)
kumulativni_minimumi = np.zeros((20, 100000))
srednji_kumulativ = np.array([0] * itot)
starija = np.zeros((broj_jedinki, broj_fajlova))
stariji_vrednosti = np.array([0]*broj_jedinki)
mladja = np.zeros((broj_jedinki, broj_fajlova))
mladji_vrednosti = np.array([0]*broj_jedinki)
roditeljski_indexi = np.array([0]*broj_roditelja)
pomocni = np.array([False]*broj_jedinki)
tok_optimizacije = np.zeros((20, 100000))

#optimizaciona funkcija
def cost_fja(x):
    rezultat = 0
    rezultat = velicina_memorije - np.matmul(x, s)
    if rezultat >= 0:
        return int(rezultat)
    else:
        return velicina_memorije

print("Algoritam je zapoceo sa radom... Potrebno je da se zavrsi svih 20 pokretanja algoritma...")
for pokretanje in range(broj_pokretanja):
    minimum = velicina_memorije
    for jedinka in range(broj_jedinki):
        for p in range(broj_fajlova):
            starija[jedinka][p] = random.randint(0, 1)
        stariji_vrednosti[jedinka] = cost_fja(starija[jedinka])
    for i in range(50):
        brojac = 0
        for p in range(broj_jedinki):
            pomocni[p] = False
        while brojac < broj_roditelja:
            prvi_roditelj = random.randint(0, broj_jedinki - 1)
            drugi_roditelj = random.randint(0, broj_jedinki - 1)
            if prvi_roditelj == drugi_roditelj or pomocni[prvi_roditelj] == True or pomocni[drugi_roditelj] == True:
                postoji = True
            if postoji == False:
                opt_fja1 = cost_fja(starija[prvi_roditelj])
                opt_fja2 = cost_fja(starija[drugi_roditelj])
                if opt_fja1 > opt_fja2:
                    pomocni[drugi_roditelj] = True
                    roditeljski_indexi[brojac] = drugi_roditelj
                else:
                    pomocni[prvi_roditelj] = True
                    roditeljski_indexi[brojac] = prvi_roditelj
                brojac = brojac + 1
            if postoji == True:
                postoji = False
        index = 0
        while index < broj_jedinki:
            if postoji == True:
                postoji = False
            prvi_roditelj = random.randint(0, broj_roditelja - 1)
            drugi_roditelj = random.randint(0, broj_roditelja - 1)
            if prvi_roditelj == drugi_roditelj or random.uniform(0, 1) > UKRSTANJE:
               postoji = True
            if postoji == False:
                granica = random.randint(0, broj_fajlova - 1)
                bit_promene = 0
                while bit_promene < broj_fajlova:
                    if bit_promene > granica:
                        mladja[index][bit_promene] = starija[roditeljski_indexi[drugi_roditelj]][bit_promene]
                    else:
                        mladja[index][bit_promene] = starija[roditeljski_indexi[prvi_roditelj]][bit_promene]
                    bit_promene = bit_promene + 1
                verovatnoca_mutacije = random.uniform(0, 1)
                if verovatnoca_mutacije < MUTACIJA:
                    pozicija_mutacije = random.randint(0, broj_fajlova - 1)
                    if mladja[index][pozicija_mutacije] != 1:
                        mladja[index][pozicija_mutacije] = 1
                    else:
                        mladja[index][pozicija_mutacije] = 0
                mladji_vrednosti[index] = cost_fja(mladja[index])
                if mladji_vrednosti[index] < minimum:
                    for p in range(broj_fajlova):
                        najbolje_resenje[p] = mladja[index][p]
                    minimum = mladji_vrednosti[index]
                    if minimum < najbolji_minimum:
                        for p in range(broj_fajlova):
                            najbolje_resenje_za_sve[p] = mladja[index][p]
                        najbolji_minimum = minimum
                tok_optimizacije[pokretanje][index + broj_jedinki * i] = mladji_vrednosti[index]
                kumulativni_minimumi[pokretanje][index + broj_jedinki * i] = minimum
                index = index + 1
        starija = copy.deepcopy(mladja)
        stariji_vrednosti = mladji_vrednosti
    print("Zavrseno pokretanje broj " + str(pokretanje+1))

#racunanje srednjeg kumulativa
for j in range(itot):
    pomocna = 0
    for i in range(broj_pokretanja):
        pomocna = pomocna + kumulativni_minimumi[i][j]
    pomocna = pomocna / broj_pokretanja
    srednji_kumulativ[j] = pomocna

#ispis
print("Najbolje resenje za sva pokretanja - raspored fajlova je :")
print(najbolje_resenje_za_sve)
print("Najbolje resenje cost f-je u svih 20 pokretanja je " + str(najbolji_minimum))

#crtanje grafika
plt.figure()
for p in range(broj_pokretanja):
    plt.loglog(np.arange(0, itot, 1), kumulativni_minimumi[p])
plt.show()

plt.figure()
plt.loglog(np.arange(0, itot, 1), srednji_kumulativ)
plt.show()
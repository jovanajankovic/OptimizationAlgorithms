from dataclasses import dataclass
import math
import numpy as np
import random

s = (2.424595205726587e-01, 1.737226395065819e-01, 1.315612759386036e-01,
     1.022985539042393e-01, 7.905975891960761e-02, 5.717509542148174e-02,
     3.155886625106896e-02, -6.242228581847679e-03, -6.565183775481365e-02,
     -8.482380513926287e-02, -1.828677714588237e-02, 3.632382803076845e-02,
     7.654845872485493e-02, 1.152250132891757e-01, 1.631742367154961e-01,
     2.358469152696193e-01, 3.650430801728451e-01, 5.816044173713664e-01,
     5.827732223753571e-01, 3.686942505423780e-01)

#inicijalizacija konstanti i promenljivih
PI = math.pi
itot = 1000
velicina_populacije = 60
broj_tacaka = 20
vektor_resenje = 0
min_opt_fja = 1000
F = 0.8
CR = 0.9
R0 = 15
D = 6
iteracija = 0
k = 0
jeste = False

#inicijalizacija nizova
x_koordinata = np.array([0.0]*broj_tacaka)
y_koordinata = np.array([0.0]*broj_tacaka)
x = []*velicina_populacije
y = []*velicina_populacije
x_niz = np.array([0.0]*(velicina_populacije*D))

# x = (xp1, yp1, xp2, yp2, A1, A2)
@dataclass
class Vektor:
    xp1: float
    yp1: float
    xp2: float
    yp2: float
    A1: float
    A2: float
    def __init__(self, xp1=0.0, yp1=0.0, xp2=0.0, yp2=0.0, A1=0.0, A2=0.0):
        self.xp1 = xp1
        self.yp1 = yp1
        self.xp2 = xp2
        self.yp2 = yp2
        self.A1 = A1
        self.A2 = A2

#inicijalizacija koordinata tacaka
for i in range(broj_tacaka):
    x_koordinata[i] = R0 * math.cos((2 * PI * i) / broj_tacaka)
    y_koordinata[i] = R0 * math.sin((2 * PI * i) / broj_tacaka)

#inicijalizacija pocetnog niza
for i in range(velicina_populacije):
    xp1 = random.uniform(-15, 15)
    yp1 = random.uniform(-15, 15)
    xp2 = random.uniform(-15, 15)
    yp2 = random.uniform(-15, 15)
    A1 = random.random()
    A2 = random.random()
    x.append(Vektor(xp1, yp1, xp2, yp2, A1, A2))
    x_niz[i * D + 0] = xp1
    x_niz[i * D + 1] = yp1
    x_niz[i * D + 2] = xp2
    x_niz[i * D + 3] = yp2
    x_niz[i * D + 4] = A1
    x_niz[i * D + 5] = A2

#optimizaciona funkcija
def cost_fja(vektor):
    zbir = 0
    prvi_koren = math.sqrt(math.pow(vektor.xp1, 2) + math.pow(vektor.yp1, 2))
    drugi_koren = math.sqrt(math.pow(vektor.xp2, 2) + math.pow(vektor.yp2, 2))
    if prvi_koren < R0 and drugi_koren < R0:
        for i in range(broj_tacaka):
            zbir += math.pow((vektor.A1 / math.sqrt(math.pow((x_koordinata[i] - vektor.xp1), 2) + math.pow((y_koordinata[i] - vektor.yp1), 2)) +
            vektor.A2 / math.sqrt(math.pow((x_koordinata[i] - vektor.xp2), 2) + math.pow((y_koordinata[i] - vektor.yp2), 2)) - s[i]), 2)
        return zbir
    else:
        return 100

#pomocna funkcija - z = xa + F*(xb - xc)
def medjuresenje(x_a, x_b, x_c):
    z_xp1 = x_a.xp1 + F*(x_b.xp1 - x_c.xp1)
    z_yp1 = x_a.yp1 + F*(x_b.yp1 - x_c.yp1)
    z_xp2 = x_a.xp2 + F*(x_b.xp2 - x_c.xp2)
    z_yp2 = x_a.yp2 + F*(x_b.yp2 - x_c.yp2)
    z_A1 = x_a.A1 + F*(x_b.A1 - x_c.A1)
    z_A2 = x_a.A2 + F*(x_b.A2 - x_c.A2)
    medju_resenje = Vektor(z_xp1, z_yp1, z_xp2, z_yp2, z_A1, z_A2)
    return medju_resenje

print("Algoritam je poceo sa izvrsavanjem...")
#implementacija algoritma
while iteracija < itot:
    while k < velicina_populacije:
        flag = False
        pozicija1 = random.randint(0, velicina_populacije - 1)
        pozicija2 = random.randint(0, velicina_populacije - 1)
        pozicija3 = random.randint(0, velicina_populacije - 1)
        if pozicija1 == pozicija2 or pozicija1 == pozicija3 or pozicija2 == pozicija3 or pozicija1 == k or pozicija2==k or pozicija3 == k:
            flag = True
        if not flag:
            x_a = x[pozicija1]
            x_b = x[pozicija2]
            x_c = x[pozicija3]
            R = random.randint(0, D - 1)
            z = medjuresenje(x_a, x_b, x_c)
            z_niz = np.array([0.0] * D)
            pomocni_niz = np.array([0.0] * D)
            z_niz[0] = z.xp1
            z_niz[1] = z.yp1
            z_niz[2] = z.xp2
            z_niz[3] = z.yp2
            z_niz[4] = z.A1
            z_niz[5] = z.A2
            for m in range(D):
                r = random.uniform(0, 1)
                if r < CR or R == m:
                    pomocni_niz[m] = z_niz[m]
                else:
                    pomocni_niz[m] = x_niz[k * D + m]
            pomocni = Vektor(pomocni_niz[0], pomocni_niz[1], pomocni_niz[2], pomocni_niz[3], pomocni_niz[4], pomocni_niz[5])
            cost_fja1 = cost_fja(pomocni)
            cost_fja2 = cost_fja(x[k])
            if cost_fja1 < cost_fja2:
                if cost_fja1 < min_opt_fja:
                    min_opt_fja = cost_fja1
                    vektor_resenje = Vektor(pomocni.xp1, pomocni.yp1, pomocni.xp2, pomocni.yp2, pomocni.A1, pomocni.A2)
                y.append(pomocni)
                if min_opt_fja <= 1e-14:
                    jeste = True
                    break
            else:
                if cost_fja2 < min_opt_fja:
                    min_opt_fja = cost_fja2
                    vektor_resenje = Vektor(x[k].xp1, x[k].yp1, x[k].xp2, x[k].yp2, x[k].A1, x[k].A2)
                y.append(x[k])
                if min_opt_fja <= 1e-14:
                    jeste = True
                    break
            k = k + 1
    if jeste:
        break
    x = []
    for m in range(velicina_populacije):
        x.append(Vektor(y[m].xp1, y[m].yp1, y[m].xp2, y[m].yp2, y[m].A1, y[m].A2))
        x_niz[m * D + 0] = y[m].xp1
        x_niz[m * D + 1] = y[m].yp1
        x_niz[m * D + 2] = y[m].xp2
        x_niz[m * D + 3] = y[m].yp2
        x_niz[m * D + 4] = y[m].A1
        x_niz[m * D + 5] = y[m].A2
    iteracija = iteracija + 1
    k = 0
    y = []

#ispis resenja
print("Resenje oblika x = (xp1, yp1, xp2, yp2, A1, A2) je : (" + str(vektor_resenje.xp1) + ", " + str(vektor_resenje.yp1) + ", " + str(
    vektor_resenje.xp2) + ", " + str(vektor_resenje.yp2) + ", " + str(vektor_resenje.A1) + ", " + str(
    vektor_resenje.A2) + ")")
print("Minimalna vrednost optimizacione funkcije je : " + str(min_opt_fja))
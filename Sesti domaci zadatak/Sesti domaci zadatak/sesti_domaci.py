# uslov za max broj servera u ormaru
# x11 + x12 + x13 + x14 <=10
# x21 + x22 + x23 + x24 <=16
# x31 + x32 + x33 + x34 <=8

#uslovi za max snagu u ormaru
# 480x11 + 650x12 + 580x13 + 390x14 <=6800
# 480x21 + 650x22 + 580x23 + 390x24 <=8700
# 480x31 + 650x32 + 580x33 + 390x34 <= 4300

#uslovi za max broj servera istog tipa
# x11 + x21 + x31<=18
# x12 + x22 + x32 <=15
# x13 + x23 + x33 <= 23
# x14 + x24 + x34 <=12

# x11,x12,x13,x14  x21,x22,x23,x24   x31,x32,x33,x34

import numpy as np
import scipy.optimize as opt
import math
import copy

#funkcija za proveru da li je odredjeni broj celog tipa ili je ipak u pitanju realan broj
def is_integer_num(n):
    if isinstance(n,int):
        return True
    if isinstance(n,float):
        return n.is_integer()
    return False

#u matrici A 12 kolona(promenljive) i 10 vrsta kao 10 uslove
A=np.array([[1,1,1,1,0,0,0,0,0,0,0,0],
            [0,0,0,0,1,1,1,1,0,0,0,0],
            [0,0,0,0,0,0,0,0,1,1,1,1],
            [480,650,580,390,0,0,0,0,0,0,0,0],
            [0,0,0,0,480,650,580,390,0,0,0,0],
            [0,0,0,0,0,0,0,0,480,650,580,390],
            [1,0,0,0,1,0,0,0,1,0,0,0],
            [0,1,0,0,0,1,0,0,0,1,0,0],
            [0,0,1,0,0,0,1,0,0,0,1,0],
            [0,0,0,1,0,0,0,1,0,0,0,1]])

b = np.array([10,16,8,6800,8700,4300,18,15,23,12])

f = np.array([310,380,350,285,310,380,350,285,310,380,350,285])

result = opt.linprog(-f, A, b)

print("Raspored servera po ormarima - necelobrojna  resenja:")
print(result.x)
print("Maximum funkcije(maksimalni racunarski kapacitet) sa necelobrojnim resenjima broja servera je:" + str(-result.fun))

current = -1
x_check = result.x
maximum = 0
temp = np.float32(np.array([0]*12))

#inicijalizacija temp niza s kojim je dalje radjena obrada
for i in range(12):
    val = np.float32(x_check[i])
    temp[i] = val.item()

#pamcenje pozicija na mestima gde je potrebno uraditi proveru broja iz opsega -3 do +4
info = np.array([0]*12)

for i in range(12):
    if temp[i] <= 1e-8:
        temp[i] = round(temp[i])
        continue
    if math.ceil(temp[i])-temp[i] <= 1e-5:
        temp[i] = math.ceil(temp[i])
        continue
    info[i] = i

#niz u koji postavjam roundovane vrednosti i s kojim se dalje radi obrada
novi_niz = np.array([0]*12)

for i in range(12):
    novi_niz[i] = temp[i]

#promenljive u koje uzimaju opseg od -3 do +4
x_int_1 = -1
x_int_2 = -1
x_int_3 = -1
x_int_4 = -1
x_int_5 = -1
x_int_6 = -1

#popunjavanje onim vrednostima koje su bile realna resenja kako bih pretrazila njihovu okolinu -3 +4
for i in range(12):
    if info[i] != 0:
        if x_int_1 == -1:
            x_int_1 = novi_niz[info[i]]
        elif x_int_2 == -1:
            x_int_2 = novi_niz[info[i]]
        elif x_int_3 == -1:
            x_int_3 = novi_niz[info[i]]
        elif x_int_4 == -1:
            x_int_4 = novi_niz[info[i]]
        elif x_int_5 == -1:
            x_int_5 = novi_niz[info[i]]
        elif x_int_6 == -1:
            x_int_6 = novi_niz[info[i]]


#pomocni niz prilikom radjenja obrade
niz = np.array([0]*12)

#finalni niz koji sadrzi celobrojna resenja
finalni_niz = np.array([0]*12)
flaga = -1
flagb = -1
flagc = -1
flagd = -1
flage = -1
flagf = -1

for xa in np.arange(x_int_1-3, x_int_1+4, 1):
    if xa < 0:
        continue
    for xb in np.arange(x_int_2 - 3, x_int_2 + 4, 1):
        if xb < 0:
            continue
        for xc in np.arange(x_int_3 - 3, x_int_3 + 4, 1):
            if xc < 0:
                continue
            for xd in np.arange(x_int_4 - 3, x_int_4 + 4, 1):
                if xd < 0:
                    continue
                for xe in np.arange(x_int_5 - 3, x_int_5 + 4, 1):
                    if xe < 0:
                        continue
                    for xf in np.arange(x_int_6 - 3, x_int_6 + 4, 1):
                        if xf < 0:
                            continue
                        for j in range(12):
                            if info[j] != 0:
                                if flaga == -1:
                                    niz[j] = xa
                                    flaga=1
                                elif flagb == -1:
                                    niz[j] = xb
                                    flagb=1
                                elif flagc == -1:
                                    niz[j] = xc
                                    flagc = 1
                                elif flagd == -1:
                                    niz[j] = xd
                                    flagd = 1
                                elif flage == -1:
                                    niz[j] = xe
                                    flage = 1
                                elif flagf == -1:
                                    niz[j] = xf
                                    flagf = 1
                            else:
                                niz[j] = novi_niz[j]
                        res = np.matmul(A, niz)
                        if np.all(res <= b):
                            suma = 0
                            for m in range(12):
                                suma += niz[m] * f[m]
                            if suma >= maximum:
                                maximum = suma
                                finalni_niz = copy.deepcopy(niz)
                        flaga = -1
                        flagb = -1
                        flagc = -1
                        flagd = -1
                        flage = -1
                        flagf = -1


print("Raspored servera po ormarima - celobrojna resenja:")
print(finalni_niz)
print("Maximum funkcije(maksimalni racunarski kapacitet) sa celobrojnim resenjima broja servera je:" + str(maximum))


# ISPISI RADI PROVERE

"""print("ispis na kraju")
for i in range(12):
    print(temp[i])

print("Pozicije")
for i in range(12):
    print(info[i])

print("Ispis novog niza")
for i in range(12):
    print(novi_niz[i]) """


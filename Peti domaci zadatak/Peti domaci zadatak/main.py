import numpy as np
import scipy.optimize as opti
import matplotlib.pyplot as plot

# np.random.seed()
# random_broj = np.random.randint(-10,10)
# print (f'Random broj:{random_broj}')
# pocetni_tezinski_faktori=[random_broj]*10

PI = np.pi
N = 5
pocetni_tezinski_faktori = []
y_t = []
y_o = []
maxiter = 25000

for i in range(10):
    pocetni_tezinski_faktori.append(2)

def trening_fja(x_in):
    return np.sin(PI * x_in) / 2

def y_out(x_in, w):
    zbir = 0.0
    i = 0
    xk = []

    for i in range(N):
        xk.append(0)

    for i in range(N):
        xk[i] = x_in * w[i]
        xk[i] = np.tanh(xk[i])

    for i in range(N):
        zbir += xk[i] * w[i + 5]

    return np.tanh(zbir)

def optimizaciona_fja(w):
    x_in = 1.0
    zbir = 0.0
    razlika = 0.0
    for elem in w:
        if elem < -10 or elem > 10:
            zbir += 2000

    while x_in >= -1.0:
        razlika = y_out(x_in, w) - trening_fja(x_in)
        zbir += pow(razlika, 2)
        x_in -= 0.1
    return np.sqrt(zbir)


resenje = opti.minimize(optimizaciona_fja, pocetni_tezinski_faktori, method='nelder-mead',
                        options={'xatol': 1e-14, 'maxiter': maxiter})

print(resenje.message)
print('Vrednost optimizacione funkcije : ' + str(resenje.fun))

index = 0
while index < N + 5:
    print("w" + str(index + 1) + " " + "{:.15f} ".format(resenje.x[index]))
    index = index + 1

w = resenje.x
xplot = np.arange(-1.0, 1.0, 0.1)
for x in xplot:
    y_o.append(y_out(x, w))
for x in xplot:
    y_t.append(trening_fja(x))
plot.figure()
plot.plot(xplot, y_t, label="trening_fja")
plot.plot(xplot, y_o, label="y_out")
plot.legend()
plot.show()

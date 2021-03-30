import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy import special

fig = plt.figure()
x = np.arange(0, 20, 0.05)
plt.plot(x,scipy.special.spherical_jn(1, x),label = "n = 1")
plt.plot(x,scipy.special.spherical_jn(2, x),label = "n = 2")
plt.legend()
plt.show()





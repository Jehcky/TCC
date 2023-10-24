import numpy as np
from matplotlib import pyplot as plt

def my_dist(x):
    return np.exp(-x ** 2)

x = np.arange(-100, 100)
p = my_dist(x)
plt.plot(x, p)
plt.show()
from cProfile import label
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('bmh')

np.random.seed(0)

x = range(0, 23)
y = [0.5, 2, 4.5, 4.2, 2, 1.5, 1.4, 3, 4, 3.4, 2, 1, 1.2, 3.2, 4.6, 3.6, 2, 0.7, 1.1, 2.4, 4.7, 4.3, 2.7]
z = (2 - np.log(y)) + np.random.rand(23)
w = (np.sqrt(y)*2) + np.random.rand(23)

y[22] = np.nan

plt.plot(x, y, marker='o', label='s')
plt.plot(x, z, '--', marker='v', label='r1',)
plt.plot(x, w, '--', marker='s', color='green', label='r2',)
plt.legend()
plt.show()


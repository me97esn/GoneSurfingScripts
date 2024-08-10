import numpy as np
import matplotlib.pyplot as plt
import json
import matplotlib.animation as animation
import ifft
import datetime
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

X = np.array([[0, 0], [1, 0] ])
Y = np.array([[0,0], [1,0]])
Z = np.array([[10,10],[10,20]])

fig = plt.figure(figsize=plt.figaspect(0.5))
samples_3d_plot = fig.add_subplot(1, 2, 1, projection='3d')
samples_3d_plot.plot_surface(X, Y, Z, cmap = plt.cm.coolwarm)

plt.show()

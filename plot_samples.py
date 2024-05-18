import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import json
import matplotlib.animation as animation

f = open('samples.json')

fig = plt.figure(figsize = (120,100))
ax = plt.axes(projection='3d')
# ax.set_xlim([xmin, xmax])
ax.set_zlim([0, 50])
# These dimensions have to match the dimensions of the data

x = np.arange(0, 100, 1)
y = np.arange(0, 100,1) 

X, Y = np.meshgrid(x, y)
data = json.load(f)
Z = np.array(data[0])
surf = ax.plot_surface(X, Y, Z, cmap = plt.cm.cividis)

# Set axes label
ax.set_xlabel('x', labelpad=20)
ax.set_ylabel('y', labelpad=20)
ax.set_zlabel('z', labelpad=200)

for i in range(1, len(data)):
    Z = np.array(data[i])
    ax.plot_surface(X, Y, Z, cmap = plt.cm.cividis)
    plt.pause(0.1)

plt.show()

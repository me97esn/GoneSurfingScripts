import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import json
import matplotlib.animation as animation

f = open('wave_samples.json')

data = json.load(f)
fig = plt.figure(figsize = (len(data[0][0]),len(data[0])))
ax = plt.axes(projection='3d')
# ax.set_xlim([xmin, xmax])

x = np.arange(0, len(data[0][0]), 1)
y = np.arange(0, len(data[0]),1) 

X, Y = np.meshgrid(x, y)
Z = np.array(data[0])
surf = ax.plot_surface(X, Y, Z, cmap = plt.cm.cividis)

# Set axes label
ax.set_xlabel('x', labelpad=20)
ax.set_ylabel('y', labelpad=20)
ax.set_zlabel('z', labelpad=200)
start_frame = 752
while True:
   for i in range(1, len(data)):
       ax.clear()
       ax.set_xlabel('Frame: ' + str(i+start_frame))
       ax.set_zlim([0, 100])
       ax.set_ylim([0, 150])
       ax.set_xlim([0, 150])
       Z = np.array(data[i])
       ax.plot_surface(X, Y, Z, cmap = plt.cm.cividis)
       plt.pause(0.01)
   
plt.show()

import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import json
f = open('samples.json')

fig = plt.figure(figsize = (12,10))
ax = plt.axes(projection='3d')

x = np.arange(0, 100, 1)
y = np.arange(0, 100,1) 

X, Y = np.meshgrid(x, y)
data_first_frame = json.load(f)[0]
# print("num of samples x: ", len(data_first_frame[0]))
# print(X)
# for x in X:
#     print(x)
# Z = np.sin(X)*np.cos(Y)
Z = np.array(data_first_frame)
print("Z:",Z)
surf = ax.plot_surface(X, Y, Z, cmap = plt.cm.cividis)

# Set axes label
ax.set_xlabel('x', labelpad=20)
ax.set_ylabel('y', labelpad=20)
ax.set_zlabel('z', labelpad=200)

plt.show()

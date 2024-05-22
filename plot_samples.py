import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import json
import matplotlib.animation as animation
from mpl_toolkits.mplot3d.axes3d import get_test_data

# set up a figure twice as wide as it is tall
fig = plt.figure(figsize=plt.figaspect(0.5))

f = open('wave_samples.json')

data = json.load(f)

ax0 = fig.add_subplot(1, 2, 2, projection='3d')
X0, Y0, Z0 = get_test_data(0.05)
ax0.plot_wireframe(X0, Y0, Z0, rstride=10, cstride=10)

# 3d plot of the samples
# fig = plt.figure(figsize = (len(data[0][0]),len(data[0])))
# fig, (ax1, ax2) = plt.subplots(2, 1)
# fig.suptitle('3D plot of the samples')
# set up the Axes for the first plot
ax = fig.add_subplot(1, 2, 1, projection='3d')
# ax = plt.axes(projection='3d')
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
       # plt.pause(1000)

# fft
# frequencies = np.fft.fftn(data)

# filtered_frequencies = []
# for i in range(len(frequencies)):
#     if i < 20 or i > 2570:
#         filtered_frequencies.append(frequencies[i])
#     else:
#         filtered_frequencies.append(0)

# plt.show()

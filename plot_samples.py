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

# 3d plot of examples
ax0 = fig.add_subplot(1, 2, 2, projection='3d')

# 3d plot of the samples
# set up the Axes for the first plot
ax = fig.add_subplot(1, 2, 1, projection='3d')
 
for axis in [ax, ax0]:
    axis.set_zlim([0, 100])
    axis.set_ylim([0, 150])
    axis.set_xlim([0, 150])

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
        # plot 1
        ax.clear()
        ax.set_xlabel('Frame: ' + str(i+start_frame))

        # get the 2d array of all of the samples for this frame
        Z = np.array(data[i])
        ax.plot_surface(X, Y, Z, cmap = plt.cm.cividis)

        # plot 2
        X0, Y0, Z0 = get_test_data(0.05)
        ax0.plot_wireframe(X, Y, Z, rstride=10, cstride=10)

        plt.pause(0.01)
# fft
# frequ encies = np.fft.fftn(data)

# filtered_frequencies = []
# for i in range(len(frequencies)):
#     if i < 20 or i > 2570:
#         filtered_frequencies.append(frequencies[i])
#     else:
#         filtered_frequencies.append(0)

# plt.show()

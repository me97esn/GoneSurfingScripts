import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import json
import matplotlib.animation as animation
from mpl_toolkits.mplot3d.axes3d import get_test_data

def filter_frequencies(data):
    frequencies = np.fft.fftn(data)
    filtered_frequencies = []
    for i, z in enumerate(frequencies):
        z_arr = []
        for ii,y in enumerate(z):
            y_arr = []
            for iii,x in enumerate(y):
                if  (ii < 20 or ii > 2570):
                    y_arr.append(x)
                else:
                    y_arr.append(0)
            z_arr.append(y_arr)
        filtered_frequencies.append(z_arr)
    return np.fft.ifftn(filtered_frequencies)

# set up a figure twice as wide as it is tall
fig = plt.figure(figsize=plt.figaspect(0.5))

f = open('wave_samples.json')

data = json.load(f)
filtered_data = filter_frequencies(data)


filtered_3d_plot = fig.add_subplot(1, 2, 2, projection='3d')
samples_3d_plot = fig.add_subplot(1, 2, 1, projection='3d')
 
for axis in [samples_3d_plot, filtered_3d_plot]:
    axis.set_zlim([0, 100])
    axis.set_ylim([0, 150])
    axis.set_xlim([0, 150])

x = np.arange(0, len(data[0][0]), 1)
y = np.arange(0, len(data[0]),1)

X, Y = np.meshgrid(x, y)

# Set axes label
samples_3d_plot.set_xlabel('x', labelpad=20)
samples_3d_plot.set_ylabel('y', labelpad=20)
samples_3d_plot.set_zlabel('z', labelpad=200)
start_frame = 752
while True:
    for i in range(1, len(data)):
        # plot 1, samples

        samples_3d_plot.clear()
        samples_3d_plot.set_xlabel('Frame: ' + str(i+start_frame))

        # get the 2d array of all of the samples for this frame
        Z = np.array(data[i])
        samples_3d_plot.plot_surface(X, Y, Z, cmap = plt.cm.cividis)

        # plot 2, fft
        filtered_3d_plot.clear()
        Z2 = np.array(filtered_data[i])
        # filtered_3d_plot.plot_wireframe(X, Y, Z2, rstride=10, cstride=10)
        filtered_3d_plot.plot_surface(X, Y, Z2, cmap = plt.cm.cividis)

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

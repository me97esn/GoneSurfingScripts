import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import json
import matplotlib.animation as animation
from mpl_toolkits.mplot3d.axes3d import get_test_data



def filter_frequencies(data):

    num_of_frames = len(data)
    num_of_rows = len(data[0])
    num_of_columns = len(data[0][0])

    frequencies = np.fft.fftn(data)
    filtered_frequencies = []
    for i, z in enumerate(frequencies):
        z_arr = []
        for ii,y in enumerate(z):
            y_arr = []
            for iii,x in enumerate(y):
                if  (iii < 20 or iii > num_of_columns - 20) :
                    y_arr.append(x)
                else:
                    y_arr.append(0)
            z_arr.append(y_arr)
        filtered_frequencies.append(z_arr)
    return np.fft.ifftn(filtered_frequencies)

# set up a figure twice as wide as it is tall
fig = plt.figure(figsize=plt.figaspect(0.5))
# plt.rcParams["figure.figsize"] = [7.00, 3.50]
# plt.rcParams["figure.autolayout"] = True

f = open('wave_samples.json')

data = json.load(f)
filtered_data = filter_frequencies(data)


filtered_3d_plot = fig.add_subplot(1, 2, 2, projection='3d')
samples_3d_plot = fig.add_subplot(1, 2, 1, projection='3d')
plot_2d = fig.add_subplot(2, 2, 2)

print("Data length: ", len(data))
print("Data[0] length: ", len(data[0]))
print("Data[0][0] length: ", len(data[0][0]))
# print(dir(samples_3d_plot))
    # axis.set_aspect("equal")

x = np.arange(0, len(data[0][0]), 1)
y = np.arange(0, len(data[0]),1)

X, Y = np.meshgrid(x, y)

plt.show(block=False)
# Set axes label
samples_3d_plot.set_xlabel('x', labelpad=20)
samples_3d_plot.set_ylabel('y', labelpad=20)
samples_3d_plot.set_zlabel('z', labelpad=200)
start_frame = 752
while True:
    for i in range(1, len(data)):
        # plot 1, samples

        samples_3d_plot.clear()
        filtered_3d_plot.clear()
        plot_2d.clear()

        for axis in [samples_3d_plot, filtered_3d_plot]:
            axis.set_zlim3d(0, 60)
            axis.set_ylim3d(0, 150)
            axis.set_xlim3d(0, 150)

        plot_2d.set_ylim(0, 150)
        plot_2d.set_xlim(0, 150)

        samples_3d_plot.set_xlabel('Frame: ' + str(i+start_frame))

        # get the 2d array of all of the samples for this frame
        Z = np.array(data[i])
        samples_3d_plot.plot_surface(X, Y, Z, cmap = plt.cm.cividis)

        # plot 2, fft
        # filtered_3d_plot.clf()
        Z2 = np.array(filtered_data[i])
        filtered_3d_plot.plot_surface(X, Y, Z2, cmap = plt.cm.cividis)

        plot_2d.plot(data[i][0], color='blue')
        plot_2d.plot(filtered_data[i][0], color='red')

        plt.pause(0.01)
# fft
# frequ encies = np.fft.fftn(data)

# filtered_frequencies = []
# for i in range(len(frequencies)):
#     if i < 20 or i > 2570:
#         filtered_frequencies.append(frequencies[i])
#     else:
#         filtered_frequencies.append(0)


import numpy as np
import matplotlib.pyplot as plt
import json
import matplotlib.animation as animation
import iift

f = open('wave_samples.json')
data = json.load(f)

def wave_height(frame, x, y):
    "TODO: should use my own ifft implementation here!"
    return  data[frame][x][y]

def recreate_samples(frequencies):
    "Loop through all of the frequencies and recreate the samples"
    result = []
    for z,y,x in frequencies:
        result.append(wave_height(z, x, y))

def filter_frequencies(data, include_number_of_columns = 30, include_number_of_rows = 30, include_number_of_frames = 30):
    "Convert to frequency domain and filter out most of the middle frequencies. Then convert back to time domain."

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
                if  (iii < include_number_of_columns or iii > num_of_columns - include_number_of_columns) and (ii < include_number_of_rows or ii > num_of_rows - include_number_of_rows)and (i < include_number_of_frames or i > num_of_frames - include_number_of_frames):
                    y_arr.append(x)
                else:
                    y_arr.append(0)
            z_arr.append(y_arr)
        filtered_frequencies.append(z_arr)
        # print(filtered_frequencies)
    return filtered_frequencies

# set up a figure twice as wide as it is tall
fig = plt.figure(figsize=plt.figaspect(0.5))


frequencies = filter_frequencies(data)
filtered_data = np.fft.ifftn(frequencies)



filtered_3d_plot = fig.add_subplot(1, 2, 2, projection='3d')
samples_3d_plot = fig.add_subplot(1, 2, 1, projection='3d')
plot_2d = fig.add_subplot(3, 1, 2)
plot_2d_2 = fig.add_subplot(2, 2, 2)

print("Data length: ", len(data))
print("Data[0] length: ", len(data[0]))
print("Data[0][0] length: ", len(data[0][0]))

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
        plot_2d_2.clear()

        for axis in [samples_3d_plot, filtered_3d_plot]:
            axis.set_zlim3d(0, 150)
            axis.set_ylim3d(0, 150)
            axis.set_xlim3d(0, 150)

        plot_2d.set_ylim(0, 150)
        plot_2d.set_xlim(0, 150)
        plot_2d_2.set_ylim(15, 25)
        plot_2d_2.set_xlim(0, 150)

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
        # TODO: should plot values from my own implementation of iift3 here!

        # Also plot the middle of the ocean
        plot_2d_2.plot(data[i][30], color='blue')
        plot_2d_2.plot(filtered_data[i][30], color='red')

        plt.pause(0.01)

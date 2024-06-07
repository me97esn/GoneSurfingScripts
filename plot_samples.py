import numpy as np
import matplotlib.pyplot as plt
import json
import matplotlib.animation as animation
import ifft
import datetime

f = open('wave_samples.json')
data = json.load(f)

# TODO: load the frequencies file, and convert all of the frequency arrays to complex numbers
frequencies_file = open('wave_frequencies_subset.json')
frequencies_data = json.load(frequencies_file)
freqs_complex = [np.array([[complex(z[0], z[1]) for z in arr] for arr in frame_frequencies]) for frame_frequencies in frequencies_data['frequencies_per_frame']]

print("Frequencies: ", freqs_complex)
exit()
print("TODO: open the frequencies file and use that instead of the samples file")

def wave_height(frame, x, y, frequencies):

    return iift.ifft3(frame, y, x, frequencies, len(frequencies),len(frequencies[0]),len(frequencies[0][0]))
    # return  data[frame][y][x]

def wave_height2(x, y, frequencies):
    return iift.ifft2(x, y, frequencies, len(frequencies),len(frequencies[0]))

# set up a figure twice as wide as it is tall
fig = plt.figure(figsize=plt.figaspect(0.5))

print("Data length: ", len(data))
print("Data[0] length: ", len(data[0]))
print("Data[0][0] length: ", len(data[0][0]))


#filtered_3d_plot = fig.add_subplot(1, 2, 2, projection='3d')
samples_3d_plot = fig.add_subplot(1, 2, 1, projection='3d')
plot_2d = fig.add_subplot(3, 1, 2)
plot_2d_2 = fig.add_subplot(2, 2, 2)

# Setup the dimensions of the plot
x = np.arange(0, len(data[0][0]), 1)
y = np.arange(0, len(data[0]),1)
X, Y = np.meshgrid(x, y)

plt.show(block=False)
samples_3d_plot.set_xlabel('x', labelpad=20)
samples_3d_plot.set_ylabel('y', labelpad=20)
samples_3d_plot.set_zlabel('z', labelpad=200)
start_frame = 752

# Filter the frequencies of all of the frames
number_of_freqs = 15
frequencies_all_frames = [np.fft.fftn(frame) for frame in data]
filtered_frequencies_all_frames = [np.array([[z for zi, z in enumerate(arr) if zi < number_of_freqs or zi >= len(arr)-number_of_freqs] for arr in frame_frequencies]) for frame_frequencies in frequencies_all_frames]

while True:
    for frame in range(1, len(data)):
        # First, clear the plots and then set the limits to clear them but restart them in the same dimensions each time
        samples_3d_plot.clear()
        #filtered_3d_plot.clear()
        plot_2d.clear()
        plot_2d_2.clear()

        for axis in [samples_3d_plot]:
            axis.set_zlim3d(0, 150)
            axis.set_ylim3d(0, len(data[0]))
            axis.set_xlim3d(0, len(data[0][0]))

        plot_2d.set_xlim(0, len(data[0][0]))
        plot_2d.set_ylim(15, 25)

        plot_2d_2.set_xlim(0, len(data[0][0]))
        plot_2d_2.set_ylim(15, 25)

        frame_frequencies = np.fft.fftn(data[frame])
        frame_frequencies_1d = np.fft.fftn(data[frame][0])

        samples_3d_plot.set_xlabel('Original samples, frame: ' + str(frame+start_frame))
        #filtered_3d_plot.set_xlabel('filtered samples, using numpy.fft.fftn')

        # get the 2d array of all of the samples for this frame
        Z = np.array(data[frame])
        samples_3d_plot.plot_surface(X, Y, Z, cmap = plt.cm.cividis)

        plot_2d.set_title('Original samples, and numpy ifft for the filtered frequencies, for one column')
        plot_2d.plot(data[frame][0], color='blue')
        plot_2d.plot(np.fft.ifftn(frame_frequencies_1d), color='red')

        plot_2d_2.set_title('Original samples, and my own ifft2 implementation for the filtered frequencies, for one column')

        lenX = len(data[frame])
        lenY = len(data[frame][0])
        # filtered_frame_frequencies = np.array([[z for zi, z in enumerate(arr) if zi < number_of_freqs or zi >= len(arr)-number_of_freqs] for arr in frame_frequencies])
        # print("frame frequencies[0]: ", frame_frequencies[0])
        recreated_column_data = [ ifft.ifft2(0, y, filtered_frequencies_all_frames[frame], lenX,lenY, number_of_freqs) for y in range(lenY)]
        # recreated_column_data = [ ifft.ifft2(0, y, filtered_frame_frequencies, lenX,lenY, number_of_freqs) for y in range(lenY)]

        plot_2d_2.plot(data[frame][0], color='blue')
        plot_2d_2.plot(recreated_column_data, color='red')
        plt.pause(0.01)

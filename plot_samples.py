import numpy as np
import matplotlib.pyplot as plt
import json
import matplotlib.animation as animation
import iift
import datetime

f = open('wave_samples.json')
data = json.load(f)

def wave_height(frame, x, y, frequencies):

    return iift.ifft3(frame, y, x, frequencies, len(frequencies),len(frequencies[0]),len(frequencies[0][0]))
    # return  data[frame][y][x]

def wave_height2(x, y, frequencies):
    return iift.ifft2(x, y, frequencies, len(frequencies),len(frequencies[0]))

def recreate_samples(frequencies2d):
    "Loop through all of the frequencies and recreate the samples"
    result = []
    for xi, x in enumerate(frequencies2d):
        row = []
        result.append(row)
        for yi, y in enumerate(x):
                row.append(wave_height2(xi, yi, frequencies2d))
    return result


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
        # TODO: most of the frequencies are zero. How should I skip them, so that they won't waste memory?
    return filtered_frequencies

# set up a figure twice as wide as it is tall
fig = plt.figure(figsize=plt.figaspect(0.5))

print("Data length: ", len(data))
print("Data[0] length: ", len(data[0]))
print("Data[0][0] length: ", len(data[0][0]))

frequencies = filter_frequencies(data)

filtered_data = np.fft.ifftn(frequencies)

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
        # TODO: filter these frequencies


        # Then plot them


        samples_3d_plot.set_xlabel('Original samples, frame: ' + str(frame+start_frame))
        #filtered_3d_plot.set_xlabel('filtered samples, using numpy.fft.fftn')

        # get the 2d array of all of the samples for this frame
        Z = np.array(data[frame])
        samples_3d_plot.plot_surface(X, Y, Z, cmap = plt.cm.cividis)

        # plot 2, fft
        Z2 = np.array(filtered_data[frame])
        #filtered_3d_plot.plot_surface(X, Y, Z2, cmap = plt.cm.cividis)
        #
        plot_2d.set_title('Original samples, and numpy ifft for the filtered frequencies, for one column')
        # plot_2d.plot(data[frame][0], color='blue')
        # plot_2d.plot(filtered_data[frame][0], color='red')
        plot_2d.plot(np.fft.ifftn(frame_frequencies[frame])[0], color='red')
        

        # plot_2d_2.set_title('Original samples, and my own ifft2 implementation for the filtered frequencies, for one column')
        # samples_column = data[frame][0]
        # plot_2d_2.plot(samples_column, color='blue')
        # recreated_column_data = [ iift.ifft2(0, y, frequencies[frame], len(data[frame]),len(data[frame][0])) for y in range(len( samples_column  ))]
        # # print(recreated_column_data)
        # # TODO: only the first sample is correct. The rest are wrong. Why?
        # plot_2d_2.plot(recreated_column_data, color='red')
        plt.pause(0.01)

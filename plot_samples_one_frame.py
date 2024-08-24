import numpy as np
import matplotlib.pyplot as plt
import json
import matplotlib.animation as animation
import ifft
import datetime
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

frame = 752

# X = np.array([[0, 1], [2, 3]])
# Y = np.array([[0,1], [2,3]])
# Z = np.array([[10,10],[20,20]])

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    if(len(lst) % n != 0):
        _lst = lst[0: -1]
    else:
        _lst = lst
    for i in range(0, len(_lst), n):
        yield _lst[i:i + n]

def plot_bobj_to_json_data():
    f = open(f'/hdd/gone_surfing_exports/medium_wave_left/tmp/{frame}.json')
    data = json.load(f)
    x_coordinates = np.array(data['x_coordinates'])
    y_coordinates = np.array(data['y_coordinates'])
    x_coordinates = np.array(data['coordinates'])[:,0]
    y_coordinates = np.array(data['coordinates'])[:,1]
    z_coordinates= data['z_coordinates']

    X = np.array(list(chunks(x_coordinates, 2)))
    Y = np.array(list(chunks(y_coordinates, 2)))
    Z = np.array(list(chunks(z_coordinates, 2)))

    fig = plt.figure(figsize=plt.figaspect(0.5))
    samples_3d_plot = fig.add_subplot(1, 2, 1, projection='3d')
    samples_3d_plot.set_zlim3d(-20,50)
    samples_3d_plot.scatter(X, Y, Z, marker='o', linewidths=0.01, edgecolors='black', s=0.1)  

def plot_samples():
    f = open('/hdd/gone_surfing_exports/medium_wave_left/tmp_samples/height-per-frame.json')
    data = json.load(f)[f'{frame}']
    x_coordinates = np.array(data['coordinates'])[:,0]
    y_coordinates = np.array(data['coordinates'])[:,1]
    z_coordinates= np.array(data['samples'])

    X = np.array(list(chunks(x_coordinates, 2)))
    Y = np.array(list(chunks(y_coordinates, 2)))
    Z = np.array(list(chunks(z_coordinates, 2)))

    fig = plt.figure(figsize=plt.figaspect(0.5))
    samples_3d_plot = fig.add_subplot(1, 2, 1, projection='3d')
    samples_3d_plot.set_zlim3d(-20,50)
    samples_3d_plot.scatter(X, Y, Z, marker='o', linewidths=0.1, edgecolors='black', s=0.1)

def flatten_2d_array(array):
    return [item for sublist in array for item in sublist]

def plot_samples_from_blender_sampling():
    f = open('/home/emil/workspace/GoneSurfingScripts/wave_samples.json')
    data = json.load(f)
    coordinates_data = np.array(data['coordinates'][0])
    samples_data = data['samples'][0]
    coordinates = np.array(flatten_2d_array(coordinates_data))
    x = coordinates[:,0]
    y = coordinates[:,1]
    z = flatten_2d_array(samples_data)

    X = np.array(list(chunks(x, 2)))
    Y = np.array(list(chunks(y, 2)))
    Z = np.array(list(chunks(z, 2)))

    fig = plt.figure(figsize=plt.figaspect(0.5))
    samples_3d_plot = fig.add_subplot(1, 2, 1, projection='3d')
    samples_3d_plot.set_zlim3d(-20,50)
    samples_3d_plot.scatter(X, Y, Z, marker='o', linewidths=5, edgecolors='black', s=0.1)


def plot_samples_from_blender_fft_ifft():
    f = open('/home/emil/workspace/GoneSurfingScripts/wave_samples.json')
    data = json.load(f)
    # Convert to the frequency domain using np
    all_frequencies = np.fft.fft2(data['samples'][0])
    lenX = len(all_frequencies)
    lenY = len(all_frequencies[0])

    # Convert back using my own implementation
    ifft_samples = [[ ifft.ifft2(x, y, all_frequencies, lenX,lenY, 5,5,5) for y in range(lenY)] for x in range(lenX)]
    coordinates_data = np.array(data['coordinates'][0])
    coordinates = np.array(flatten_2d_array(coordinates_data))
    x = coordinates[:,0]
    y = coordinates[:,1]
    z = flatten_2d_array(ifft_samples)

    X = np.array(list(chunks(x, 2)))
    Y = np.array(list(chunks(y, 2)))
    Z = np.array(list(chunks(z, 2)))

    fig = plt.figure(figsize=plt.figaspect(0.5))
    samples_3d_plot = fig.add_subplot(1, 2, 1, projection='3d')
    samples_3d_plot.set_zlim3d(-20,50)
    samples_3d_plot.scatter(X, Y, Z, marker='o', linewidths=5, edgecolors='black', s=0.1)






def plot_fft_to_ifft():
    f = open('/hdd/gone_surfing_exports/medium_wave_left/tmp_samples/height_frequencies.json')
    frequencies_data = json.load(f)


    number_of_frequencies_to_include = frequencies_data['number_of_frequencies_to_include']
    frequencies_per_frame = frequencies_data['frequencies_per_frame']

    # Frequencies for all frames
    freqs_complex = [np.array([[complex(z[0], z[1]) for z in arr] for arr in frame_frequencies]) for frame_frequencies in frequencies_data['frequencies_per_frame']]

    number_of_frequencies_to_include = frequencies_data['number_of_frequencies_to_include']
    number_of_rows_to_include = frequencies_data['number_of_rows_to_include']
    lenX = int(frequencies_data['len_x'] / 1 )# Subset to make this faster
    lenY = int(frequencies_data['len_y'] / 1)
    frequencies_first_frame = freqs_complex[0]

    recreated_column_data = [[ ifft.ifft2(x, y, frequencies_first_frame, lenX,lenY, number_of_frequencies_to_include, number_of_rows_to_include, number_of_rows_to_include ) for y in range(lenY)] for x in range(lenX)]
    samples_3d_plot = plt.figure().add_subplot(111, projection='3d')

    x = np.arange(0, len(recreated_column_data), 1)
    y = np.arange(0, len( recreated_column_data[0] ),1)
    # y = np.arange(0, 1,1)
    X, Y = np.meshgrid(x, y)

    samples_3d_plot.scatter(X, Y, recreated_column_data)

# plot_bobj_to_json_data()
# plot_samples()
# plot_fft_to_ifft()
plot_samples_from_blender_sampling()
plot_samples_from_blender_fft_ifft()

# Split X, Y and Z into array of pairs, since that's what plot_surface expects

# # plt.imshow(grid_x, extent=(0,1,0,1), origin='lower')
# # plt.imshow(height, extent=(0,1,0,1), origin='lower')
# # plot two 1d arrays of float values, x and y from the points array
# # plt.plot(points[:,0], points[:,1], 'k.', ms=1)
# # plt.plot(coordinates, 'k.', ms=1)
# #
# #
# # # set up a figure twice as wide as it is tall
# #
# #
# #
# # #filtered_3d_plot = fig.add_subplot(1, 2, 2, projection='3d')
# Scale the plot to make it more similar to the blender view
# #
# # # Setup the dimensions of the plot
# # x = np.arange(0, len(data[0][0]), 1)
# # y = np.arange(0, len(data[0]),1)
# # X, Y = np.meshgrid(data['coordinates'])
# #
# plt.show(block=False)
# # samples_3d_plot.set_xlabel('x', labelpad=20)
# # samples_3d_plot.set_ylabel('y', labelpad=20)
# # samples_3d_plot.set_zlabel('z', labelpad=200)
# #
# # Z = np.array(data[frame])
# # samples_3d_plot.plot_surface(X, Y, Z, cmap = plt.cm.c)
# print('coordinates[:,0]', np.array(coordinates)[:,0])
plt.show()

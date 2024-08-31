import numpy as np
import matplotlib.pyplot as plt
import json
import matplotlib.animation as animation
import ifft
import datetime
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

frame = 752

plt.rcParams['figure.figsize'] = [40, 4]

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
    """
    This function can actually plot both the samples created from bobj files, and from the file created by running ray_cast in blender
    """
    f = open('/hdd/gone_surfing_exports/medium_wave_left/tmp_samples/dx-per-frame.json')
    data = json.load(f)['752']
    coordinates_data = np.array(data['coordinates'])
    z = data['samples']
    coordinates = np.array(coordinates_data)
    x = coordinates[:,0]
    y = coordinates[:,1]

    X = np.array(list(chunks(x, 2)))
    Y = np.array(list(chunks(y, 2)))
    Z = np.array(list(chunks(z, 2)))

    fig = plt.figure(figsize=plt.figaspect(0.5))
    samples_3d_plot = fig.add_subplot(1, 2, 1, projection='3d')
    # samples_3d_plot.set_zlim3d(-20,50)
    samples_3d_plot.scatter(X, Y, Z, marker='o', linewidths=5, edgecolors='black', s=0.1)


def plot_samples_from_blender_fft_ifft():
    print('------------ plot_samples_from_blender_fft_ifft ------------')
    f = open('/hdd/gone_surfing_exports/medium_wave_left/wave_samples.json')
    data = json.load(f)
    data_samples = data['samples'][0]
    # Convert to the frequency domain using np
    all_frequencies = np.fft.fft2(data_samples)
    lenX = len(all_frequencies)
    lenY = len(all_frequencies[0])

    # Convert back using my own implementation
    number_of_frequencies_to_include = 75
    number_of_rows_to_include = 35

    ifft_samples = [[ ifft.ifft2(x, y, all_frequencies, lenX,lenY, number_of_frequencies_to_include,number_of_rows_to_include,number_of_rows_to_include) for y in range(lenY)] for x in range(lenX)]
    coordinates_data = np.array(data['coordinates'][0])
    coordinates = np.array(flatten_2d_array(coordinates_data))
    x = coordinates[:,0]
    y = coordinates[:,1]
    z = flatten_2d_array(ifft_samples)
    z2 = flatten_2d_array(data_samples)

    X = np.array(list(chunks(x, 2)))
    Y = np.array(list(chunks(y, 2)))
    Z_ifft = np.array(list(chunks(z, 2)))
    Z_original = np.array(list(chunks(z2, 2)))

    fig = plt.figure()
    samples_3d_plot = fig.add_subplot(1, 1, 1, projection='3d')
    samples_3d_plot.set_zlim3d(-20,50)

    # Plot the original and the ifft samples in the same plot
    samples_3d_plot.scatter(X, Y, Z_ifft, marker='o', linewidths=5, edgecolors='black', s=1)
    samples_3d_plot.scatter(X, Y, Z_original, marker='o', linewidths=5, edgecolors='red', s=1)


def convert_3d_array_of_real_and_imaginary_to_complex_grid(real_and_imaginary_array):
    """
    real_and_imaginary_array: [
        [
            [
                [182.5802234634454, 0.0], # complex number, real and imaginary part
                [-10.198202656846245, 6.80804848440372], ...] # complex number, real and imaginary part
            ] # column
        ] # row

    """
    # print(np.array(real_and_imaginary_array))
    # print('row: ',np.array(real_and_imaginary_array[0]))
    # print('col: ',np.array(real_and_imaginary_array[0][0]))
    # print('real: ',np.array(real_and_imaginary_array[0][0][0]))
    # print('complex: ',np.array(real_and_imaginary_array[0][0][1]))

    # [ print( row ) for row in real_and_imaginary_array]

    return np.array([[complex(col[0], col[1]) for col in row ] for row in real_and_imaginary_array])


# TODO: Should be able to plot the frequencies in the same way as the samples
def plot_fft_to_ifft():
    """
    The data looks as the following: 
"frequencies_per_frame": [[[[182.5802234634454, 0.0], [-10.198202656846245, 6.80804848440372], 
    """
    print('------------ plot_fft_to_ifft ------------')
    f = open('/hdd/gone_surfing_exports/medium_wave_left/tmp_samples/height_frequencies.json')
    frequencies_data = json.load(f)


    # number_of_frequencies_to_include = 50
    # number_of_rows_to_include = 50

    frequencies_per_frame = frequencies_data['frequencies_per_frame']
    frequencies_first_frame = frequencies_per_frame[0]

    # Frequencies for all frames
    freqs_complex = convert_3d_array_of_real_and_imaginary_to_complex_grid(frequencies_first_frame)

    lenX = int(frequencies_data['len_x']  )
    lenY = int(frequencies_data['len_y'] )
    Z = np.fft.ifft2( freqs_complex )
    # _Z = [[ ifft.ifft2(x, y, frequencies_first_frame, lenX,lenY, number_of_frequencies_to_include, number_of_rows_to_include, number_of_rows_to_include ) for y in range(lenY)] for x in range(lenX)]
    # Z_flat = flatten_2d_array(_Z)


    # TODO: These coordinates aren't correct, 
    x = np.linspace(-6, 6, lenX)
    y = np.linspace(-6, 6, lenY)

    X, Y = np.meshgrid(x, y)

    # Z = np.array(list(chunks(_Z, 2)))

    samples_3d_plot = plt.figure().add_subplot(111, projection='3d')


    samples_3d_plot.scatter(X, Y, Z)

# plot_bobj_to_json_data()
# plot_samples()
plot_fft_to_ifft()
# plot_samples_from_blender_sampling()
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

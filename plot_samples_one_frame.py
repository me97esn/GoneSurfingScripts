import numpy as np
import matplotlib.pyplot as plt
import json
import matplotlib.animation as animation
import ifft
import datetime
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import time

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


def plot_wave_samples_json():
    f = open('/hdd/gone_surfing_exports/medium_wave_left/wave_samples.json')
    data = json.load(f)
    data_samples = data['samples'][0]
    # Convert to the frequency domain using np
    all_frequencies = np.fft.fft2(data_samples)
    lenX = len(all_frequencies)
    lenY = len(all_frequencies[0])

    # Convert back using my own implementation
    number_of_frequencies_to_include = 87
    number_of_rows_to_include = 40

    print('running ifft.ifft2 for %f * %f = %f number of samples' % (lenX, lenY, lenX*lenY))
    start_time = time.time()
    ifft_samples = [[ ifft.ifft2_include_all(x, y, all_frequencies, lenX,lenY) for y in range(lenY)] for x in range(lenX)]
    # ifft_samples = [[ ifft.ifft2(x, y, all_frequencies, lenX,lenY, number_of_frequencies_to_include,number_of_rows_to_include,number_of_rows_to_include) for y in range(lenY)] for x in range(lenX)]
    print("Time to run ifft: ", time.time() - start_time)
    X,Y = coordinates_from_samples_file()
    z_ifft = flatten_2d_array(ifft_samples)
    z_original = flatten_2d_array(data_samples)

    Z_ifft = np.array(list(chunks(z_ifft, 2)))
    Z_original = np.array(list(chunks(z_original, 2)))

    fig = plt.figure()
    samples_3d_plot = fig.add_subplot(1, 1, 1, projection='3d')
    samples_3d_plot.set_zlim3d(-20,50)

    # Plot the original and the ifft samples in the same plot
    samples_3d_plot.scatter(X, Y, Z_ifft, marker='o', linewidths=5, edgecolors='black', s=1)
    samples_3d_plot.scatter(X, Y, Z_original, marker='o', linewidths=5, edgecolors='red', s=1)
    samples_3d_plot.set_title("Wave_samples.json -> np.fft -> my ifft implementation")


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

def coordinates_from_samples_file():
    f_samples = open('/hdd/gone_surfing_exports/medium_wave_left/wave_samples.json')
    data = json.load(f_samples)

    coordinates_data = np.array(data['coordinates'][0])
    coordinates = np.array(flatten_2d_array(coordinates_data))
    x = coordinates[:,0]
    y = coordinates[:,1]

    X = np.array(list(chunks(x, 2)))
    Y = np.array(list(chunks(y, 2)))

    return X, Y

def plot_height_frequencies_json():
    """
    The data looks as the following: 
"frequencies_per_frame": [[[[182.5802234634454, 0.0], [-10.198202656846245, 6.80804848440372], 
    """
    f = open('/hdd/gone_surfing_exports/medium_wave_left/tmp_samples/height_frequencies.json')
    frequencies_data = json.load(f)


    # number_of_frequencies_to_include = 50
    # number_of_rows_to_include = 50

    frequencies_per_frame = frequencies_data['frequencies_per_frame']
    frequencies_first_frame = frequencies_per_frame[0]
    shape = np.array(frequencies_first_frame).shape
    print('shape of frequencies first frame', shape)


    # Frequencies for all frames
    freqs_complex = convert_3d_array_of_real_and_imaginary_to_complex_grid(frequencies_first_frame)

    lenX = int(frequencies_data['len_x']  )
    lenY = int(frequencies_data['len_y'] )
    Z = np.fft.ifft2( freqs_complex )

    X, Y = coordinates_from_samples_file()

    samples_3d_plot = plt.figure().add_subplot(111, projection='3d')
    samples_3d_plot.set_zlim3d(-20,50)
    samples_3d_plot.scatter(X, Y, Z)

def plot_height_frequencies_struct_json():
    file = open('/hdd/gone_surfing_exports/medium_wave_left/height_frequencies_struct.json')
    f = json.load(file)[0]['f']
    freqs_complex_2d = []
    for rowObj in f:
        row = []
        freqs_complex_2d.append(row)
        for colObj in rowObj['arr']:
            row.append(complex(colObj['re'], colObj['im']))

    # TODO: re-create the 3d plot using my own ifft implementation
    # Z = np.fft.ifft2( freqs_complex_2d )
    lenX = len(f)
    lenY = len(f[0]['arr'])
    Z2 = [[ ifft.ifft2_include_all(x, y, freqs_complex_2d, lenX,lenY) for y in range(lenY)] for x in range(lenX)]

    X, Y = coordinates_from_samples_file()

    z_ifft = flatten_2d_array(Z2)

    Z_ifft = np.array(list(chunks(z_ifft, 2)))





    # Z2_pairs = np.array(Z2).reshape(np.array(X).shape)

    samples_3d_plot = plt.figure().add_subplot(111, projection='3d')
    samples_3d_plot.set_zlim3d(-20,50)
    # samples_3d_plot.scatter(X, Y, Z)
    # samples_3d_plot.scatter(X, Y, Z, marker='o', linewidths=0.1, edgecolors='black', s=0.1)
    samples_3d_plot.scatter(X, Y, Z_ifft, color='red', s=5)
    samples_3d_plot.set_title("height_frequencies_struct.json with np.ifft and my ifft implementation on top of each other")

def print_height_at_coordinates(x, y):
    file = open('/hdd/gone_surfing_exports/medium_wave_left/height_frequencies_struct.json')
    f = json.load(file)[0]['f']
    freqs_complex_2d = []
    for rowObj in f:
        row = []
        freqs_complex_2d.append(row)
        for colObj in rowObj['arr']:
            row.append(complex(colObj['re'], colObj['im']))

    # TODO: re-create the 3d plot using my own ifft implementation
    # Z = np.fft.ifft2( freqs_complex_2d )
    lenX = len(f)
    lenY = len(f[0]['arr'])
    height = ifft.ifft2_with_interpolation(x, y, freqs_complex_2d, lenX,lenY)
    print('height at coordinates: %f, %f is %f' % (x, y, height))

print_height_at_coordinates( -57, 153)
print_height_at_coordinates( -57, 152)
print_height_at_coordinates( -57, 154)
print_height_at_coordinates( -57.471939, 153.670105)
print_height_at_coordinates( -57.471939, 152.123718)
# plot_height_frequencies_json()
# plot_wave_samples_json()
# plot_height_frequencies_struct_json()

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

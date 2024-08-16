import numpy as np
import matplotlib.pyplot as plt
import json
import matplotlib.animation as animation
import ifft
import datetime
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

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

# grid_x, grid_y = np.mgrid[0:1:3j, 0:1:6j]
# print('grid_x', grid_x)
# print('grid_y', grid_y)
#
# points = np.random.rand(10, 2)
# print('points', points)
# print('points[:,0]', points[:,0]) 
# print('points[:,1]', points[:,1])
#
# print('points', points)
#
#
def plot_sample_file():
    f = open('/hdd/gone_surfing_exports/medium_wave_left/tmp/752.json')
    data = json.load(f)
    # TODO: these coordinates are not sorted. It seems that 3d plot requires sorted coordinates?
    x_coordinates = np.array(data['x_coordinates'])
    y_coordinates = np.array(data['y_coordinates'])
    # x_coordinates = [x for x,y in data['coordinates']]
    # y_coordinates = [y for x,y in data['coordinates']]
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

def plot_vertices_converted_to_samples_non_formatted():
    f = open('/hdd/gone_surfing_exports/medium_wave_left/tmp_samples/height_non_formatted.json')
    data = json.load(f)['752']
    # TODO: these coordinates are not sorted. It seems that 3d plot requires sorted coordinates?
    x_coordinates = np.array(data['coordinates'])[:,0]
    y_coordinates = np.array(data['coordinates'])[:,1]
    z_coordinates= np.array(data['samples'])
    print('x_coordinates', x_coordinates)
    print('y_coordinates', y_coordinates)
    print('z_coordinates', z_coordinates)

    # Sort the coordinates
    x_coordinates, y_coordinates, z_coordinates = zip(*sorted(zip(x_coordinates, y_coordinates, z_coordinates)))
    print('len x_coordinates', len(x_coordinates))
    X = np.array(list(chunks(x_coordinates, 2)))
    Y = np.array(list(chunks(y_coordinates, 2)))
    Z = np.array(list(chunks(z_coordinates, 2)))

    fig = plt.figure(figsize=plt.figaspect(0.5))
    samples_3d_plot = fig.add_subplot(1, 2, 1, projection='3d')
    samples_3d_plot.set_zlim3d(-20,50)
    samples_3d_plot.scatter(X, Y, Z, marker='o', linewidths=0.01, edgecolors='black', s=0.1)  
    # samples_3d_plot.plot_surface(X, Y, Z, cmap = plt.cm.coolwarm, linewidth=0, antialiased=False)


plot_sample_file()
plot_vertices_converted_to_samples_non_formatted()

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

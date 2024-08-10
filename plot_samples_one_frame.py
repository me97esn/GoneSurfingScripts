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
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

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
f = open('/hdd/gone_surfing_exports/medium_wave_left/tmp/752.json')
data = json.load(f)
height = data['height']
coordinates = np.array(data['coordinates'])
print('coordinates[10]', coordinates[:10])
x_coordinates = coordinates[:,0]
y_coordinates = coordinates[:,1]
z_values = np.array(height)

X = np.array(list(chunks(x_coordinates, 2)))
Y = np.array(list(chunks(y_coordinates, 2)))
Z = np.array(list(chunks(z_values, 2)))
print('X', X)

# Split X, Y and Z into array of pairs, since that's what plot_surface expects

# # plt.imshow(grid_x, extent=(0,1,0,1), origin='lower')
# # plt.imshow(height, extent=(0,1,0,1), origin='lower')
# # plot two 1d arrays of float values, x and y from the points array
# # plt.plot(points[:,0], points[:,1], 'k.', ms=1)
# # plt.plot(coordinates, 'k.', ms=1)
# #
# #
# # # set up a figure twice as wide as it is tall
fig = plt.figure(figsize=plt.figaspect(0.5))
# #
# #
# #
# # #filtered_3d_plot = fig.add_subplot(1, 2, 2, projection='3d')
samples_3d_plot = fig.add_subplot(1, 2, 1, projection='3d')
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
samples_3d_plot.plot_surface(X, Y, Z, cmap = plt.cm.coolwarm)
plt.show()

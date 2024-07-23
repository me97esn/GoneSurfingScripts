from scipy.interpolate import griddata
import numpy as np
#define a function
def func(x,y):
    return (x**2+y**2+(x*y)**2)**2

#generate random points
rng = np.random.default_rng()
points = rng.random((10, 2)) # 6x2 array
print('points:',points)

#generate values from the points generated above
values = func(points[:,0], points[:,1])

print('values:',values)

#generate grid data using the points and values above
grid_a = griddata(points, values, np.array([[0.5,0.4],[0.4,0.5],[0.5,0.5]]), method='cubic')
print("result:",grid_a)

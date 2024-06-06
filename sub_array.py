import numpy.matlib
import numpy as np
a1 = np.arange(4)

array_2d = np.arange(30).reshape(3, 10)
print(array_2d)

array_2d_2 = np.array([[z for zi, z in enumerate(arr) if zi < 3 or zi >= len(arr)-3] for arr in array_2d])
print (array_2d_2)


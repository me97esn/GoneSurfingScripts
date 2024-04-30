import numpy as np
a = [1,1.6, 0]
# a = np.mgrid[:3, :3, :3][0]
f = np.fft.fftn(a )

print("Original values:\n",a)
print()
print("Fouriere transform: \n",f)


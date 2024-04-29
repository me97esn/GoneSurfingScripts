import numpy as np
a = [1,1.1]
# a = np.mgrid[:3, :3, :3][0]
f = np.fft.fftn(a )

print(a)
print(f)


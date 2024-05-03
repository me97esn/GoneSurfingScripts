import numpy as np
import scipy.fft as scipy_fft


a = [1, 1.6, 0 ]
# a = np.mgrid[:3, :3, :3][0]
f = np.fft.fftn(a )


print('cos:', scipy_fft.dct(a))
print('sin:', scipy_fft.idst(a))
print()
ift = np.fft.ifftn(f)
print()
# print(f.complex)
print("Original values:\n",a)
print()
print("Fouriere transform: \n",f)
print("Inverse fft: \n", ift)


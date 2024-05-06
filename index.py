import numpy as np

a = np.array([1, 1.6, 0])
print(a)
b = np.fft.fft(a)


def ifft2(x, y, fourierCoefficients):
    ""
    result = 0.0j
    M = len(fourierCoefficients)
    N = len(fourierCoefficients[0])

    for m in range(M):
        for n in range(N):
            result = result + fourierCoefficients[m][n]*np.exp(2*np.pi*1j*(m*x/M + n*y/N))/(M*N)
    return result.real


def ifft(t, fourierCoefficients):
    ""
    n = len(fourierCoefficients)
    result = 0.0j
    for m in range(n):
        result = result + fourierCoefficients[m]*np.exp(2*np.pi*1j*m*t/n)/n
    return result.real



print(ifft(0, b))
print(ifft(1, b))
print(ifft(2, b))

# fill an array with zero imaginary numbers
# c = np.linspace(0, n-1, num=n)*1.0j
# for t in range(n):
#     c[t] = 0.0
#     for k in range(n):
#         c[t] = c[t] + b[k]*np.exp(2*np.pi*1j*k*t/n)/n
# print(c)

a2 = np.array([[0,1,0], [1, 1.1, 1.2], [1, 1, 1]])
b2 = np.fft.fftn(a2)

print("-----------------")
print("Original 2d array\n",a2)
print("Fouriere transformed 2d array:\n",b2)
print(ifft2(1, 1, b2))

import numpy as np

a = np.array([1, 1.6, 0])
n = len(a)
print(a)
b = np.fft.fft(a)

def ifft(t):
    ""
    result = 0.0j
    for k in range(n):
        result = result + b[k]*np.exp(2*np.pi*1j*k*t/n)/n
    return result

print(ifft(0))
print(ifft(1))
print(ifft(2))

# fill an array with zero imaginary numbers
c = np.linspace(0, n-1, num=n)*1.0j
for t in range(n):
    c[t] = 0.0
    for k in range(n):
        c[t] = c[t] + b[k]*np.exp(2*np.pi*1j*k*t/n)/n
print(c)


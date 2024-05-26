import numpy as np

def ifft2(x, y, fourierCoefficients, lenX, lenY):
    result = 0.0j

    for m in range(lenX):
        for n in range(lenY):
            print("m: ", m, "n: ", n, "lenX:", lenX, "lenY:", lenY)

            print()
            fourierCoefficient = fourierCoefficients[m][n]
            result = result + fourierCoefficient*np.exp(2*np.pi*1j*(m*x/lenX + n*y/lenY))/(lenX*lenY)
    return result.real


def ifft(t, fourierCoefficients):
    ""
    n = len(fourierCoefficients)
    result = 0.0j
    for m in range(n):
        result = result + fourierCoefficients[m]*np.exp(2*np.pi*1j*m*t/n)/n
    return result.real

# TODO: create iift3 function

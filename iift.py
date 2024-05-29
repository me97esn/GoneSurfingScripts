import numpy as np
# https://numpy.org/doc/stable/reference/routines.fft.html
def ifft2(x, y, fourierCoefficients, lenX, lenY):
    result = 0.0j

    for m in range(lenX):
        for n in range(lenY):
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

def ifft3(a, b, c, fourierCoefficients, lenA, lenB, lenC):
    # print("a: ", a, "b: ", b, "c: ", c)
    result = 0.0j
    # return fourierCoefficients[a][b][c]
    for l in range(lenA):
        for m in range(lenB):
            for n in range(lenC):
                fourierCoefficient = fourierCoefficients[l][m][n]
                result = result + fourierCoefficient*np.exp(2*np.pi*1j*(l*a/lenA + m*b/lenB + n*c/lenC))/(lenA*lenB*lenC)
    return result.real



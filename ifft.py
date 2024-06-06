import numpy as np
import datetime
# https://numpy.org/doc/stable/reference/routines.fft.html
def ifft2(x, y, fourierCoefficients, lenX, lenY, numberOfFrequenciesToInclude=30):
    time_start = datetime.datetime.now()
    # print("x: ", x, "y: ", y, "lenX: ", lenX, "lenY: ", lenY)
    result = 0.0j

    for i, m in enumerate( range(lenX)):
        # temporarilly create a filterered subset of the fourier coefficients
        for ii, n in enumerate( range(lenY)):
            fourierCoefficient = fourierCoefficients[m][n]
            # print("m: ", m, "n: ", n, "fourierCoefficient: ", fourierCoefficient, "x: ", x, "y: ", y, "lenX: ", lenX, "lenY: ", lenY)
            # Low frequencies are at the beginning of the list
            if  ii < numberOfFrequenciesToInclude:
                result = result + fourierCoefficient*np.exp(2*np.pi*1j*(m*x/lenX + n*y/lenY))/(lenX*lenY)

            # High frequencies are at the end of the list
            if ii >= lenY - numberOfFrequenciesToInclude:
                result = result + fourierCoefficient*np.exp(2*np.pi*1j*(m*x/lenX + n*y/lenY))/(lenX*lenY)
    time_end = datetime.datetime.now()
    c = time_end - time_start

    # print("Time taken: ", c.total_seconds(), " seconds")
    return result.real


def ifft(t, fourierCoefficients):
    ""
    n = len(fourierCoefficients)
    result = 0.0j
    for m in range(n):
        result = result + fourierCoefficients[m]*np.exp(2*np.pi*1j*m*t/n)/n
    return result.real

# NOTE: This function does not work as expected
def ifft3(a, b, c, fourierCoefficients, lenA, lenB, lenC):
    # print("a: ", a, "b: ", b, "c: ", c)
    result = 0.0j
    print(".", end="")
    # return fourierCoefficients[a][b][c]
    for l in range(lenA):
        for m in range(lenB):
            for n in range(lenC):
                fourierCoefficient = fourierCoefficients[l][m][n]
                result = result + fourierCoefficient*np.exp(2*np.pi*1j*(l*a/lenA + m*b/lenB + n*c/lenC))/(lenA*lenB*lenC)
    return result.real



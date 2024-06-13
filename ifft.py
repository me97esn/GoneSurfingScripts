import numpy as np
import datetime
# https://numpy.org/doc/stable/reference/routines.fft.html
def ifft2(x, y, fourierCoefficients, lenX, lenY, numberOfFrequenciesToInclude=30, numberOfRowsToInclude=30):
    """Note: lenX and lenY should be the total number of samples BEFORE subtracting the ignored frequencies"""
    # time_start = datetime.datetime.now()
    result = 0.0j
    # print("frame frequencies length: ", len(fourierCoefficients))
    # print("frame frequencies[0] length: ", len(fourierCoefficients[0]))
    #
    number_to_skip = lenY - numberOfFrequenciesToInclude * 2
    for m in range(lenX):
        if m < numberOfRowsToInclude:
            for n in range(len(fourierCoefficients[0])):
                # print("n: ", n, "m: ", m)
                fourierCoefficient = fourierCoefficients[m][n]
                # Low frequencies are at the beginning of the list
                if  n < numberOfFrequenciesToInclude:
                    result = result + fourierCoefficient*np.exp(2*np.pi*1j*(m*x/lenX + n*y/lenY))/(lenX*lenY)
                    # print("--- fourierCoefficient: ", fourierCoefficient)
                else:
                    # Middle frequencies are not included in the list
                    _n = n + number_to_skip
                    # print("=== fourierCoefficient after skipping: ", fourierCoefficient)

                    # High frequencies are at the end of the list
                    result = result + fourierCoefficient*np.exp(2*np.pi*1j*(m*x/lenX + _n*y/lenY))/(lenX*lenY)
    # ti    me_end = datetime.datetime.now()
    # c = time_end - time_start

    # print("Time taken: ", c.total_seconds(), " seconds")
        # exit()
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



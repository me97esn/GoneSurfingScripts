import numpy as np
import datetime
# https://numpy.org/doc/stable/reference/routines.fft.html
def ifft2(x, y, fourierCoefficients, lenX, lenY, numberOfFrequenciesToInclude=30, numberOfRowsToIncludeBottom=2, numberOfRowsToIncludeTop=10):
    """Note: lenX and lenY should be the total number of samples BEFORE subtracting the ignored frequencies"""
    result = 0.0j
    number_to_skip = lenY - numberOfFrequenciesToInclude * 2
    numberOfRowsToSkip = lenX - numberOfRowsToIncludeBottom * 2
    print("numberOfFrequenciesToInclude: ", numberOfFrequenciesToInclude)
    print("numberOfRowsToIncludeTop: ", numberOfRowsToIncludeTop)
    print("numberOfRowsToIncludeBottom: ", numberOfRowsToIncludeBottom)

    for m in range(len(fourierCoefficients)):
        _m = m
        if m < numberOfRowsToIncludeBottom:# or m >= len(fourierCoefficients)-numberOfRowsToIncludeTop:
            print("including row: ", m) 
        elif m >= len(fourierCoefficients)-numberOfRowsToIncludeTop:
            print("second including row: ", m)
        else:
            continue
            # _m = m
            # else:
            #     _m = m + numberOfRowsToSkip
            #
        for n in range(len(fourierCoefficients[0])):
            fourierCoefficient = fourierCoefficients[m][n]
            # Low frequencies are at the beginning of the list
            if  n < numberOfFrequenciesToInclude:
                result = result + fourierCoefficient*np.exp(2*np.pi*1j*(_m*x/lenX + n*y/lenY))/(lenX*lenY)
            else:
                # Middle frequencies are not included in the list
                _n = n + number_to_skip
    
                # High frequencies are at the end of the list
                result = result + fourierCoefficient*np.exp(2*np.pi*1j*(_m*x/lenX + _n*y/lenY))/(lenX*lenY)
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


